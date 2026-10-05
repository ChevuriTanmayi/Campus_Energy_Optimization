import pandas as pd
import numpy as np
file_path = "dataset/all_buildings_power.csv"
df = pd.read_csv(file_path)
print("Dataset loaded successfully!")
print("Rows:", len(df))
print("Columns:", len(df.columns))
df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
df.drop(columns=["timestamp"], inplace=True)
print("\nDataset columns:")
print(df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nMissing values:")
print(df.isnull().sum())

# DATA CLEANING
df = df.set_index("datetime")
building_columns = [
    "Academic",
    "Boys_main",
    "Boys_backup",
    "Facilities",
    "Girls_main",
    "Girls_backup",
    "Lecture",
    "Library",
    "Mess"
]
missing_before = df[building_columns].isnull().sum()
df[building_columns] = df[building_columns].interpolate(
    method="time",
    limit=60
)
df = df.dropna(
    subset=building_columns,
    how="all"
)
missing_after = df[building_columns].isnull().sum()
print("\nMissing values BEFORE cleaning:")
print(missing_before)
print("\nMissing values AFTER cleaning:")
print(missing_after)
print("\nCleaned dataset rows:", len(df))

# MISSING VALUE ANALYSIS
missing_summary = pd.DataFrame({
    "Missing Before": missing_before,
    "Missing After": missing_after
})
missing_summary["Missing % Before"] = (
    missing_summary["Missing Before"] / len(df) * 100
)
missing_summary["Missing % After"] = (
    missing_summary["Missing After"] / len(df) * 100
)
print("\nMissing Value Summary:")
print(missing_summary.round(2))

# DUPLICATE RECORD CHECK
duplicate_count = df.index.duplicated().sum()
print("\nDuplicate timestamp records:", duplicate_count)

# INVALID / NEGATIVE VALUE CHECK
negative_values = (df[building_columns] < 0).sum()
print("\nNegative power values:")
print(negative_values)

# BUILDING-WISE ENERGY CONSUMPTION
building_totals = df[building_columns].sum().sort_values(ascending=False)
print("\nTotal Energy Consumption by Building:")
print(building_totals)
# BAR CHART
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
building_totals.plot(kind="bar")
plt.title("Total Energy Consumption by Building")
plt.xlabel("Building")
plt.ylabel("Total Power Reading")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("building_energy_comparison.png")
plt.show()

# AVERAGE POWER CONSUMPTION BY BUILDING
building_average = df[building_columns].mean().sort_values(ascending=False)
print("\nAverage Power Consumption by Building:")
print(building_average)
# BAR CHART
plt.figure(figsize=(10, 6))
building_average.plot(kind="bar")
plt.title("Average Power Consumption by Building")
plt.xlabel("Building")
plt.ylabel("Average Power (Watts)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("average_power_by_building.png")
plt.show()

# HOURLY CAMPUS POWER DEMAND
# Calculate total campus power at each timestamp
df["Total_Campus_Power"] = df[building_columns].sum(axis=1, skipna=True)
# Group readings by hour of the day
hourly_power = df.groupby(df.index.hour)["Total_Campus_Power"].mean()
print("\nAverage Campus Power by Hour:")
print(hourly_power)
# Find peak hour
peak_hour = hourly_power.idxmax()
peak_power = hourly_power.max()
print("\nPeak Power Hour:", peak_hour)
print("Peak Average Power:", round(peak_power, 2), "Watts")
# Line chart
plt.figure(figsize=(10, 6))
hourly_power.plot(kind="line", marker="o")
plt.title("Average Campus Power Demand by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Power (Watts)")
plt.xticks(range(24))
plt.grid(True)
plt.tight_layout()
plt.savefig("hourly_campus_power.png")
plt.show()

# BUILDING CONTRIBUTION DURING PEAK HOUR
peak_hour_data = df[df.index.hour == peak_hour]
peak_building_power = (
    peak_hour_data[building_columns]
    .mean()
    .sort_values(ascending=False)
)
print("\nAverage Building Power During Peak Hour:")
print(peak_building_power)
# Bar chart
plt.figure(figsize=(10, 6))
peak_building_power.plot(kind="bar")
plt.title(f"Average Building Power During Peak Hour ({peak_hour}:00)")
plt.xlabel("Building")
plt.ylabel("Average Power (Watts)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("peak_hour_building_contribution.png")
plt.show()

# ANOMALY DETECTION
hourly_campus = (
    df["Total_Campus_Power"]
    .resample("h")
    .mean()
    .dropna()
)
Q1 = hourly_campus.quantile(0.25)
Q3 = hourly_campus.quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
anomalies = hourly_campus[
    (hourly_campus < lower_bound) |
    (hourly_campus > upper_bound)
]
high_anomalies = hourly_campus[
    hourly_campus > upper_bound
]
print("\n--- ANOMALY DETECTION ---")
print("Lower Bound:", round(lower_bound, 2), "Watts")
print("Upper Bound:", round(upper_bound, 2), "Watts")
print("Total Anomalous Hours:", len(anomalies))
print("Unusually High Demand Hours:", len(high_anomalies))
print("\nTop 10 High-Demand Anomalies:")
print(high_anomalies.sort_values(ascending=False).head(10))
# Plot anomalies
plt.figure(figsize=(12, 6))
plt.plot(
    hourly_campus.index,
    hourly_campus.values,
    label="Hourly Campus Power"
)
plt.scatter(
    high_anomalies.index,
    high_anomalies.values,
    label="High-Demand Anomaly"
)
plt.title("Campus Energy Demand Anomaly Detection")
plt.xlabel("Date")
plt.ylabel("Average Power (Watts)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("campus_energy_anomalies.png")
plt.show()

# BUILDING CONTRIBUTION DURING HIGH-DEMAND ANOMALIES
anomaly_dates = high_anomalies.index
anomaly_building_power = df.loc[
    df.index.floor("h").isin(anomaly_dates),
    building_columns
].mean().sort_values(ascending=False)
print("\n--- BUILDING CONTRIBUTION DURING HIGH-DEMAND ANOMALIES ---")
print(anomaly_building_power)
plt.figure(figsize=(10, 6))
anomaly_building_power.plot(kind="bar")
plt.title("Building Contribution During High-Demand Anomalies")
plt.xlabel("Building")
plt.ylabel("Average Power (Watts)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("anomaly_building_contribution.png")
plt.show()

# ACTION PRIORITY RANKING
average_power_kw = building_average / 1000
anomaly_power_kw = anomaly_building_power / 1000
average_score = (
    average_power_kw / average_power_kw.max()
) * 100
anomaly_score = (
    anomaly_power_kw / anomaly_power_kw.max()
) * 100
# Combined priority score
priority_score = (
    0.5 * average_score +
    0.5 * anomaly_score
)
priority_table = pd.DataFrame({
    "Average Power (kW)": average_power_kw,
    "Anomaly Power (kW)": anomaly_power_kw,
    "Priority Score": priority_score
}).sort_values(
    "Priority Score",
    ascending=False
)
def assign_priority(score):
    if score >= 70:
        return "High"
    elif score >= 40:
        return "Medium"
    else:
        return "Low"
priority_table["Priority"] = priority_table["Priority Score"].apply(
    assign_priority
)
print("\n--- ACTION PRIORITY RANKING ---")
print(priority_table.round(2))
priority_table.to_csv("action_priority_ranking.csv")
# Plot
plt.figure(figsize=(10, 6))
priority_table["Priority Score"].plot(kind="bar")
plt.title("Campus Building Energy Action Priority")
plt.xlabel("Building")
plt.ylabel("Priority Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("action_priority_ranking.png")
plt.show()

# DESCRIPTIVE STATISTICS
statistics = df[building_columns].describe().T
statistics = statistics[
    ["mean", "std", "min", "max"]
]
statistics.columns = [
    "Mean (W)",
    "Std Dev (W)",
    "Minimum (W)",
    "Maximum (W)"
]
print("\n--- DESCRIPTIVE STATISTICS ---")
print(statistics.round(2))
statistics.to_csv("descriptive_statistics.csv")

# CORRELATION ANALYSIS
correlation_matrix = df[building_columns].corr()
print("\n--- CORRELATION MATRIX ---")
print(correlation_matrix.round(2))
correlation_matrix.to_csv("building_correlation_matrix.csv")
plt.figure(figsize=(10, 8))
plt.imshow(
    correlation_matrix,
    cmap="coolwarm",
    aspect="auto"
)
plt.colorbar(label="Correlation")
plt.xticks(
    range(len(building_columns)),
    building_columns,
    rotation=45,
    ha="right"
)
plt.yticks(
    range(len(building_columns)),
    building_columns
)
plt.title("Correlation Between Building Power Consumption")
plt.tight_layout()
plt.savefig("building_correlation_heatmap.png")
plt.show()
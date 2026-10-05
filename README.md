# Campus Energy Optimization Analyzer

## Overview

Campus buildings consume electricity in different patterns depending on their usage, occupancy, facilities and time of day. Understanding these patterns can help identify high-demand periods and prioritize areas where energy-saving actions may have the greatest impact.

This project analyzes historical electrical power data from an academic campus to identify:

- Building-wise power consumption patterns
- Average campus demand by hour
- Peak-demand periods
- Unusually high-demand periods using anomaly detection
- Buildings contributing most during high-demand periods
- Relationships between building power consumption
- An action-priority ranking for energy optimization

The project focuses on exploratory data analytics, anomaly detection and decision-oriented insights rather than prediction.


## Problem Statement

Campus energy consumption is distributed across multiple buildings such as academic blocks, hostels, library, dining facilities and lecture buildings.

Without analyzing the data, it can be difficult to determine:

- Which buildings have higher average power demand?
- When does campus demand reach its highest level?
- Which periods show unusually high demand?
- Which buildings contribute most during these periods?
- Which buildings should receive attention first for energy optimization?

This project uses data analytics to answer these questions.


## Dataset

The project uses the **I-BLEND (Indian Buildings Energy Consumption Dataset)** developed using electrical energy data from an academic institute campus in India.

The dataset contains electrical measurements collected at one-minute intervals from multiple campus buildings.

The combined energy file used in this project contains:

- 2,310,568 records
- 9 building power columns
- Timestamp information

### Buildings analyzed

- Academic
- Boys Main
- Boys Backup
- Facilities
- Girls Main
- Girls Backup
- Lecture
- Library
- Mess

### Data Source

I-BLEND — A campus-scale commercial and residential buildings electrical energy dataset.

Authors:
Haroon Rashid, Pushpendra Singh and Amarjeet Singh

Dataset collection:
Figshare

Dataset DOI:
10.6084/m9.figshare.c.3893581.v1

License:
CC BY 4.0

The original dataset is not included in this repository because the raw CSV file is too large for a standard GitHub repository. It can be obtained from the official I-BLEND dataset source using the DOI above.


## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib


## Data Analytics Workflow

The project follows this workflow:

Raw Data
   ↓
Data Structuring
   ↓
Data Cleaning
   ↓
Exploratory Data Analysis
   ↓
Hourly Demand Analysis
   ↓
Anomaly Detection
   ↓
Building Contribution Analysis
   ↓
Correlation Analysis
   ↓
Action Priority Ranking
   ↓
Insights & Recommendations


## Data Cleaning

The following preprocessing steps were performed:

1. Converted Unix timestamps into readable date-time values.
2. Used the timestamp as the time-series index.
3. Checked missing values for each building.
4. Interpolated short missing periods using time-based interpolation.
5. Kept longer missing periods rather than filling them blindly.
6. Checked for duplicate timestamps.
7. Checked for negative power readings.

The analysis found no duplicate timestamps and no negative power values.


## Analysis Performed

### 1. Building-wise Power Analysis

Average power consumption was calculated for each building to compare their typical demand levels.

The Academic building showed the highest average available power reading, followed by the Mess and Boys Main buildings.

### 2. Hourly Campus Demand

Power readings from available buildings were aggregated by hour to identify the typical daily demand pattern.

The highest average campus demand occurred around **6:00 AM**, at approximately **111.93 kW** based on the available building readings.

### 3. Anomaly Detection

The Interquartile Range (IQR) method was used to identify unusually high hourly campus demand.

These observations are treated as statistical high-demand anomalies and do not automatically indicate equipment faults.

### 4. Anomaly Contribution

Building-wise power values were analyzed during the identified high-demand periods.

The Academic building and Mess were the major contributors during these periods.

### 5. Correlation Analysis

Correlation analysis was performed to understand relationships between building power patterns.

Some notable relationships include:

- Boys Backup and Girls Backup: **0.84**
- Academic and Lecture: **0.69**
- Academic and Library: **0.69**
- Boys Main and Girls Main: **0.69**

These relationships indicate that some buildings show similar power-demand patterns, while others operate more independently.

### 6. Action Priority Ranking

An analytical priority score was created using:

- Average power demand
- Contribution during high-demand periods

Buildings were then classified into High, Medium and Low priority categories.

The Academic building received the highest priority score, followed by the Mess.


## Key Insights

- The Academic building has the highest average available power demand among the analyzed buildings.
- The typical campus demand profile reaches its highest average level around 6:00 AM.
- Academic and Mess buildings are important contributors during high-demand periods.
- Some hostel-related meters show strong positive relationships in their power patterns.
- Statistical anomaly detection can help identify periods that deserve further investigation.
- An action-priority ranking can help energy managers focus their initial optimization efforts on the most significant contributors.


## Recommendations

Based on the analysis, the following actions can be considered:

1. Investigate high-demand periods in the Academic building.
2. Review energy usage in dining/Mess facilities during high-demand periods.
3. Examine repeated high-demand anomalies to determine whether they are caused by occupancy, equipment usage, schedules or other operational factors.
4. Monitor buildings with high average demand more closely.
5. Combine energy data with occupancy, weather and academic calendar data in future analysis.
6. Use building-level monitoring to identify potential energy-saving opportunities.


## Project Outputs

The analysis generates:

- Building energy comparison chart
- Average power comparison chart
- Hourly campus power demand chart
- Campus energy anomaly chart
- Building contribution during anomalies
- Action priority ranking chart
- Correlation heatmap
- Action priority ranking CSV
- Descriptive statistics CSV
- Building correlation matrix CSV


## Project Structure

Campus_Energy_Optimization/
│
├── dataset/
│   └── all_buildings_power.csv
|── ChevuriTanmayi_ProjectReport.docx
├── ChevuriTanmayi_Campus_Energy_Optimization.py
├── requirements.txt
├── README.md
│
├── action_priority_ranking.csv
├── descriptive_statistics.csv
├── building_correlation_matrix.csv
│
├── building_energy_comparison.png
├── average_power_by_building.png
├── hourly_campus_power.png
├── campus_energy_anomalies.png
├── anomaly_building_contribution.png
├── action_priority_ranking.png
├── peak_hour_building_contribution.png
└── building_correlation_heatmap.png


## Limitations
* The analysis uses the available building readings at each timestamp.
* Missing building readings are not completely reconstructed.
* Therefore, campus-level power values may be lower than the actual total when some meters have missing observations.
* The IQR method identifies statistical anomalies, which should be investigated further before being considered actual faults.
* The action-priority score is an analytical scoring method created for this project and is not provided by the original dataset.
* Energy consumption can be affected by factors such as occupancy, weather and academic schedules that are not fully included in the current analysis.

## Future Scope
The project can be extended by combining the energy data with:
* Occupancy data
* Local weather data
* Academic semester calendar
* Building characteristics
Future versions could also use machine learning for energy-demand forecasting or more advanced anomaly detection.

## License and Dataset Attribution
This project uses the I-BLEND dataset created by Haroon Rashid, Pushpendra Singh and Amarjeet Singh.

The original dataset is distributed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

The dataset source and original authors should be credited when the dataset or derived analysis is reused.




from matplotlib import pyplot as plt
import pandas as pd

norm_stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly.csv'
precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_hourly.csv'

norm_stage_df = pd.read_csv(norm_stage_path, parse_dates=['End of Interval (UTC)']) #, parse_dates=['Time'])
norm_stage_df.rename(columns={'End of Interval (UTC)': 'Time'}, inplace=True)
precip_df = pd.read_csv(precip_path, parse_dates=['End of Interval (UTC)'])
precip_df.rename(columns={'End of Interval (UTC)': 'Time'}, inplace=True)

#stations = norm_stage_df['Station Code'].unique()
stations = ['CNT', 'PEL', 'CDL']
year = 2020

precip_df = precip_df[precip_df['Station Code'].isin(stations)]

fig, ax = plt.subplots(figsize=(14, 8))
for station in stations:
    station_df = norm_stage_df[norm_stage_df['Station Code'] == station]
    #station_df = station_df[station_df['Time'].dt.year == year]
    ax.plot(station_df['Time'], station_df['Value'], label=station)
    """station_precip_df = precip_df[precip_df['Station Code'] == station]
    station_precip_df = station_precip_df[station_precip_df['Time'].dt.year == year]
    ax.plot(station_precip_df['Time'], station_precip_df['Value'], label=station)"""

ax.set_xlabel('Date')
ax.set_ylabel('Normalized Stage')
ax.legend()
plt.show()
plt.close()
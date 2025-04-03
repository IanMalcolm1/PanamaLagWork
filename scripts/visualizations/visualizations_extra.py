import pandas as pd
import matplotlib.pyplot as plt
import scipy
import matplotlib.dates as mdates

# Station data (rel is for relating stage stations to stations in upstream watersheds)
stations_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\station_data\station_data.csv'
stations_rel_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\station_data\watershed_station_rel.csv'

stations_df = pd.read_csv(stations_path)
stage_stations_df = stations_df[stations_df['On_Major_River'] == 1]
stations_rel_df = pd.read_csv(stations_rel_path)

# Hydro data
precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_hourly.csv'
stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly_normalized.csv'

date_cols_precip = ['Start of Interval (UTC)', 'End of Interval (UTC)']
date_cols_stage = ['Start of Interval (UTC)', 'Time']

precip_df = pd.read_csv(precip_path, parse_dates=date_cols_precip)
stage_df = pd.read_csv(stage_path, parse_dates=date_cols_stage)

rename_cols = {
    'Start of Interval (UTC)': 'Start',
    'End of Interval (UTC)': 'End',
}

precip_df.rename(columns=rename_cols, inplace=True)
stage_df.rename(columns=rename_cols, inplace=True)

station_id = 'CDL'
start_date = pd.to_datetime("01-05-2020", dayfirst=True)
end_date = pd.to_datetime("01-01-2021", dayfirst=True)

precip_mask = (precip_df['End'] >= start_date) & (precip_df['End'] <= end_date) & (precip_df['Station Code'] == station_id)
clip_precip_df = precip_df[precip_mask]

stage_mask = (stage_df['Time'] >= start_date) & (stage_df['Time'] <= end_date) & (stage_df['Station Code'] == station_id)
clip_stage_df = stage_df[stage_mask]

# Lag Data
lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\norm_lag.csv'
lag_df = pd.read_csv(lagpath, parse_dates=['StageTime', 'PrecipTime'])

lag_df = lag_df[(lag_df['StageTime']>start_date) & (lag_df['StageTime']<end_date)]
lag_df = lag_df[lag_df['StageStation'] == station_id]




# Create the dual-axis plot
fig, ax1 = plt.subplots(figsize=(14, 8))

# Plot precipitation data on left y-axis
color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Precipitation (mm)', color=color)
ax1.plot(clip_precip_df['End'], clip_precip_df['Value'], color=color, linewidth=0.7, label='Precipitation')
ax1.tick_params(axis='y', labelcolor=color)

# Create second y-axis for stage data
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Stage (m)', color=color)
ax2.plot(clip_stage_df['Time'], clip_stage_df['Value'], color=color, linewidth=2, label='Stage')
ax2.tick_params(axis='y', labelcolor=color)

# Add local maxes
#test_stage_peaks, _ = scipy.signal.find_peaks(clip_stage_df['Value'], prominence=0.03, distance=2)
#ax2.plot(clip_stage_df['Time'].iloc[test_stage_peaks], clip_stage_df['Value'].iloc[test_stage_peaks], 'r.')

# Create combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')


# Plot peaks points
ax2.plot(lag_df['StageTime'], lag_df['StageValue'], 'ro')
ax1.plot(lag_df['PrecipTime'], lag_df['PrecipValue'], 'bo')

# Force pyplot to recalculate the limits, which is necessary for the next step
print(ax1.get_xlim(), ax1.get_ylim())
print(ax2.get_xlim(), ax2.get_ylim())

# Connect associated peaks with lines
for row in lag_df.itertuples():
    # Convert to display coordinates
    stage_display = ax2.transLimits.transform(
        (mdates.date2num(row.StageTime), row.StageValue)
    )
    precip_display = ax1.transLimits.transform(
        (mdates.date2num(row.PrecipTime), row.PrecipValue)
    )

    #convert back to ax1 data coordinates (I realize doing these steps for stage is redundant)
    stage_ax1 = ax1.transLimits.inverted().transform(stage_display)
    precip_ax1 = ax1.transLimits.inverted().transform(precip_display)

    xs = [stage_ax1[0], precip_ax1[0]]
    ys = [stage_ax1[1], precip_ax1[1]]

    ax1.plot(xs, ys, 'r--')

# Add title
plt.title(f'Precipitation and Stage at {station_id}')

# Format the x-axis to show dates nicely
fig.autofmt_xdate()
plt.tight_layout()

# Show the plot
plt.show()
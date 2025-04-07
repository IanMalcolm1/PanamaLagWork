import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal as sig
import matplotlib.dates as mdates
import context
import hydro_utils

def main():
    # Hydro data
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_hourly.csv'
    stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly_norm.csv'
    lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\norm_lag.csv'

    precip_df = hydro_utils.read_precip_data(precip_path)
    stage_df = hydro_utils.read_stage_data_norm(stage_path)
    lag_df = hydro_utils.read_lag_data(lagpath)

    # Filter data
    stage_station = 'CAN'
    precip_station = 'GAD'
    start_date = stage_df['Time'].min()
    end_date = "2028-01-01"

    precip_mask = hydro_utils.range_mask(precip_df, precip_station, start_date, end_date)
    stage_mask = hydro_utils.range_mask(stage_df, stage_station, start_date, end_date)
    lag_mask = hydro_utils.range_mask(
        lag_df, stage_station, start_date, end_date,
        time_col='StageTime', station_col='StageStation'
    )

    clip_precip_df = precip_df[precip_mask]
    clip_stage_df = stage_df[stage_mask]
    lag_df = lag_df[lag_mask]

    plot_lag_vis(clip_precip_df, clip_stage_df, lag_df, stage_station)


def plot_lag_vis(clip_precip_df, clip_stage_df, lag_df, station_id, plot_maxes=True, peaks_args={}):
    """
    Plot the lag between precipitation and stage data.

    Args:
        clip_precip_df (pd.DataFrame): DataFrame containing clipped precipitation data.
        clip_stage_df (pd.DataFrame): DataFrame containing clipped stage data.
        lag_df (pd.DataFrame): DataFrame containing lag data.
        station_id (str): Station ID to be used in the plot title.
    """
    # Create the dual-axis plot
    fig, ax1 = plt.subplots(figsize=(14, 8))

    # Plot precipitation data on left y-axis
    color = 'tab:blue'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Precipitation (mm)', color=color)
    ax1.plot(clip_precip_df['Time'], clip_precip_df['Value'], color=color, linewidth=0.7, label='Precipitation')
    ax1.tick_params(axis='y', labelcolor=color)

    # Create second y-axis for stage data
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Stage (m)', color=color)
    ax2.plot(clip_stage_df['Time'], clip_stage_df['Value'], color=color, linewidth=2, label='Stage')
    ax2.tick_params(axis='y', labelcolor=color)

    # Add local maxes
    test_stage_peaks, _ = sig.find_peaks(clip_stage_df['Value'], prominence=0.02, distance=2)
    ax2.plot(clip_stage_df['Time'].iloc[test_stage_peaks], clip_stage_df['Value'].iloc[test_stage_peaks], 'r.')

    # Create combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    # Plot peaks points
    ax2.plot(lag_df['StageTime'], lag_df['StageValue'], 'ro')
    ax1.plot(lag_df['PrecipTime'], lag_df['PrecipValue'], 'bo')

    # Force pyplot to recalculate the limits, which is necessary for the next step
    ax1.get_xlim()
    ax1.get_ylim()
    ax2.get_xlim()
    ax2.get_ylim()

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

        ax1.plot(xs, ys, 'k--')

    # Add title
    plt.title(f'Precipitation and Stage at {station_id}')

    # Format the x-axis to show dates nicely
    fig.autofmt_xdate()
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
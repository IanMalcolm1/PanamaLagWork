import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal as sig
import matplotlib.dates as mdates
import context
import hydro_utils as hutils
from norm_stage import remove_stage_outliers

USE_NORM_STAGE = False

def main():    
    # Hydro data
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_15min.csv'
    stage_path_norm = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par_norm.csv'
    stage_path_og = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par.csv'
    lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'

    precip_df = hutils.read_precip_data(precip_path, single_time_col=False)
    lag_df = hutils.read_peaks_data(lagpath)

    if USE_NORM_STAGE:
        stage_df = hutils.read_stage_data_norm(stage_path_norm)
    else:
        stage_df = hutils.read_stage_data_og(stage_path_og)
        stage_df = remove_stage_outliers(stage_df)

    # List of station ID pairs (index 0 is river station, 1 is precip station)
    station_id_pairs = [
        ['CNT', 'CNT'],
        ['PEL', 'PEL'],
        ['CDL', 'CDL'],
        ['GRM', 'ARC'],
        ['CHI', 'CHI'],
        ['CQA', 'ZAN'],
        ['CHR', 'CHR'],
        ['CAN', 'CAN'],
    ]

    for station_id_pair in station_id_pairs:
        stage_station = station_id_pair[0]
        precip_station = station_id_pair[1]

        start_date = stage_df['Time'].min()
        end_date = "2028-01-01"

        plot_lag_vis(lag_df, stage_df, precip_df, stage_station, precip_station, start_date, end_date)




def plot_lag_vis(lag_df, stage_df, precip_df, stage_station, precip_station, start_date, end_date):
    precip_mask = hutils.range_mask(precip_df, precip_station, start_date, end_date)
    stage_mask = hutils.range_mask(stage_df, stage_station, start_date, end_date)
    lag_mask = hutils.range_mask(
        lag_df, stage_station, start_date, end_date,
        time_col='StageTime', station_col='StageStation'
    )

    clip_precip_df = precip_df[precip_mask]
    clip_stage_df = stage_df[stage_mask]
    lag_df = lag_df[lag_mask]

    plot_lag_vis_inner(clip_precip_df, clip_stage_df, lag_df, stage_station, plot_maxes=False)


def plot_lag_vis_inner(precip_df, stage_df, lag_df, station_id,
                 plot_maxes=True, peaks_args={'prominence':0.02, 'distance':2}):
    """
    Plot the lag between precipitation and stage data. Assumes all dataframes are already
    clipped to the same time range and station.

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
    ax1.plot(precip_df['Time'], precip_df['Value'], color=color, linewidth=2, label='Precipitation')

    # Create second y-axis for stage data
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Stage (m)', color=color)

    # Plot stage
    ax2.plot(stage_df['Time'], stage_df['Value'], color=color, linewidth=2, label='Stage')

    # Add local maxes
    if plot_maxes:
        test_stage_peaks, _ = sig.find_peaks(stage_df['Value'], **peaks_args)
        ax2.plot(stage_df['Time'].iloc[test_stage_peaks], stage_df['Value'].iloc[test_stage_peaks], 'r.')

    # Create combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    # Plot peaks points
    lag_df_joined = pd.merge(lag_df, stage_df, left_on='StageTime', right_on='Time', suffixes=('', '_stage'), how='left')
    print(lag_df_joined.columns)
    ax2.plot(lag_df_joined['StageTime'], lag_df_joined['Value'], 'ro')
    ax1.plot(lag_df['PrecipTime'], lag_df['PrecipValue'], 'bo')

    # Force pyplot to recalculate the limits, which is necessary for the next step
    ax1.get_xlim()
    ax1.get_ylim()
    ax2.get_xlim()
    ax2.get_ylim()

    # Connect associated peaks with lines
    for row in lag_df_joined.itertuples():
        # Convert to display coordinates
        stage_display = ax2.transLimits.transform(
            (mdates.date2num(row.StageTime), row.Value)
        )
        precip_display = ax1.transLimits.transform(
            (mdates.date2num(row.PrecipTime), row.PrecipValue)
        )

        #convert back to ax1 data coordinates
        stage_ax2 = ax2.transLimits.inverted().transform(stage_display)
        precip_ax2 = ax2.transLimits.inverted().transform(precip_display)

        xs = [stage_ax2[0], precip_ax2[0]]
        ys = [stage_ax2[1], precip_ax2[1]]

        ax2.plot(xs, ys, 'k--', alpha=0.7)

    # Add title
    plt.title(f'Precipitation and Stage at Station {station_id}')

    # Format the x-axis to show dates nicely
    fig.autofmt_xdate()
    plt.tight_layout()

    # Show the plot
    plt.show()


if __name__ == "__main__":
    main()
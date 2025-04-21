import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import context
import lag_stats, precip_sums, hydro_utils as hutils


def main():
    peaks_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_15min.csv'

    peaks_df = hutils.read_peaks_data(peaks_path)
    precip_df = hutils.read_precip_data(precip_path, single_time_col=False)

    lag_df = lag_stats.make_lag_df(peaks_df)

    plot_lag_avgs_vs_precip_yearly(lag_df, precip_df)


def plot_lag_avgs_yearly(lag_df):
    lag_stats_yearly = lag_stats.lag_stats_yearly(lag_df)

    stations = lag_df['StageStation'].unique()

    for station_id in stations:
        fig, ax = plt.subplots(figsize=(14, 8))
        yearly_means_slice = lag_stats_yearly[lag_stats_yearly['StageStation'] == station_id]
        ax.plot(yearly_means_slice['Year'], yearly_means_slice['mean'], '-', label=station_id)

        ax.legend()
        plt.show()


def plot_lag_avgs_vs_precip_yearly(lag_df, precip_df):
    lag_yearly = lag_stats.lag_stats_yearly(lag_df)
    precip_yearly = precip_sums.precip_sum_yearly(precip_df)

    lag_yearly['PrecipStation'] = lag_yearly['StageStation'].map({
        'CNT': 'CNT',
        'PEL': 'PEL',
        'CDL': 'CDL',
        'GRM': 'ARC',
        'CHI': 'CHI',
        'CQA': 'ZAN',
        'CHR': 'CHR',
        'CAN': 'CAN'
    })

    precip_lag_df = pd.merge(
        lag_yearly, precip_yearly,
        left_on=['PrecipStation', 'Year'],
        right_on=['Station Code', 'Year'],
        how='left'
    )

    tableau_colors = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f',
                  '#edc949', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab']
    
    stations = precip_lag_df['StageStation'].unique().tolist()
    color_map = {stations[i]: tableau_colors[i] for i in range(len(stations))}

    precip_lag_df['color'] = precip_lag_df['StageStation'].map(color_map).astype(str)

    print(precip_lag_df.dtypes)
    

    # Plotting the lag time
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title(f'Yearly Average Lag vs Total Precipitation')

    for station_id in stations:
        station_data = precip_lag_df[precip_lag_df['StageStation'] == station_id]
        ax.plot(station_data['PrecipSum'], station_data['mean'], 'o', color=color_map[station_id], label=station_id)

    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
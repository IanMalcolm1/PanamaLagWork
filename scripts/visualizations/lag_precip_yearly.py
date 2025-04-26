import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import context
import lag_stats, scripts.precip_stats as precip_stats, hydro_utils as hutils
from colors import LAG_COLOR_MAP
import numpy as np
from numpy.polynomial.polynomial import Polynomial


def main():
    peaks_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_15min.csv'

    peaks_df = hutils.read_peaks_data(peaks_path)
    precip_df = hutils.read_precip_data(precip_path, single_time_col=False)

    lag_df = lag_stats.make_lag_df(peaks_df)

    plot_lag_avgs_vs_precip_yearly(lag_df, precip_df)
    plot_lag_avgs_vs_precip_yearly(lag_df, precip_df, {'CAN'})
    plot_lag_avgs_vs_precip_yearly(lag_df, precip_df, {'CAN', 'CHI'})


def plot_lag_avgs_yearly(lag_df):
    lag_stats_yearly = lag_stats.lag_stats_yearly(lag_df)

    stations = lag_df['StageStation'].unique()

    for station_id in stations:
        fig, ax = plt.subplots(figsize=(14, 8))
        yearly_means_slice = lag_stats_yearly[lag_stats_yearly['StageStation'] == station_id]
        ax.plot(yearly_means_slice['Year'], yearly_means_slice['mean'], '-', label=station_id)

        ax.legend()
        plt.show()


def plot_lag_avgs_vs_precip_yearly(lag_df, precip_df, station_blacklist = None, trendline_degree=1):
    lag_yearly = lag_stats.lag_stats_yearly(lag_df)
    precip_yearly = precip_stats.calc_yearly_precip(precip_df)
    
    if station_blacklist is None:
        station_blacklist = set()

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
    
    # Order stations by mean lag time
    lag_stats_df = lag_stats.lag_stats_full(lag_df)
    lag_stats_df = lag_stats_df[~lag_stats_df['StageStation'].isin(station_blacklist)]
    stations = lag_stats_df.sort_values(by='mean')["StageStation"].unique().tolist()

    # Plotting the lag time
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title(f'Yearly Average Lag vs Total Precipitation')
    ax.set_xlabel('Total Precipitation (mm)')
    ax.set_ylabel('Mean Lag (hrs)')

    precip_lag_slice = precip_lag_df[~precip_lag_df['StageStation'].isin(station_blacklist)]

    for station_id in stations:
        station_data = precip_lag_slice[precip_lag_slice['StageStation'] == station_id]
        ax.plot(
            station_data['PrecipSum'], station_data['mean'],
            'o', color=LAG_COLOR_MAP[station_id], markeredgecolor = 'black',
            label=station_id)
        
    fit_poly = Polynomial.fit(
        precip_lag_slice['PrecipSum'], precip_lag_slice['mean'], trendline_degree
    )
    x_fit = np.linspace(precip_lag_slice['PrecipSum'].min(), precip_lag_slice['PrecipSum'].max(), 100)
    y_fit = fit_poly(x_fit)

    ax.plot(x_fit, y_fit, color='black', linestyle='--', label='Trendline')

    ax.legend()
    plt.show()

    residuals = precip_lag_slice['mean'] - fit_poly(precip_lag_slice['PrecipSum'])
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_title(f'Yearly Average Lag Residuals vs Total Precipitation')
    ax.set_xlabel('Total Precipitation (mm)')
    ax.set_ylabel('Residuals (hours)')
    ax.axhline(0, color='black', linestyle='--')
    ax.plot(
        precip_lag_slice['PrecipSum'], residuals,
        'o', color='black', markeredgecolor = 'black',
        label=station_id
    )
    ax.set_ylim(-2, 2)
    plt.show()


if __name__ == '__main__':
    main()
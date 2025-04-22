from matplotlib import pyplot as plt
import context
import pandas as pd
import lag_stats as lavg
import hydro_utils as hutils
from colors import LAG_COLOR_MAP


def main():
    peaks_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'
    out_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\figures\average_lag_full1.svg'

    peaks_df = hutils.read_peaks_data(peaks_path)
    lag_df = lavg.make_lag_df(peaks_df)

    stations = lag_df['StageStation'].unique().tolist()
    print(stations)

    plot_full_avgs(lag_df, stations, out_path)
    #plot_yearly_avgs(lag_df, stations)
    #plot_monthly_avgs(lag_df, stations)


def plot_full_avgs(lag_df, stations, out_path=None):
    # Import font management
    import matplotlib.font_manager as fm
    
    full_stats = lavg.lag_stats_full(lag_df)
    full_stats.sort_values(by=['mean'], inplace=True, ascending=False)

    # Sort stations by their mean lag time
    all_stations = full_stats['StageStation'].unique().tolist()
    sorted_stations = []
    for station_id in all_stations:
        if station_id in stations:
            sorted_stations.append(station_id)

    fig, ax = plt.subplots(figsize=(14, 8))

    for i in range(len(sorted_stations)):
        station_stats = full_stats[full_stats['StageStation'] == sorted_stations[i]]
        ax.bar(
            station_stats['StageStation'], station_stats['mean'],
            color=LAG_COLOR_MAP[sorted_stations[i]], edgecolor='black',
            label=sorted_stations[i]
        )

    # Set title and axis labels with the font
    ax.set_title('Average Lag Time by Station')
    ax.set_xlabel('Station Id')
    ax.set_ylabel('Mean Lag (hrs)')
    
    plt.tight_layout()
    plt.show()

    if out_path is not None:
        plt.savefig(format='svg', fname=out_path, bbox_inches='tight')


def plot_yearly_avgs(lag_df, stations):
    yearly_stats = lavg.lag_stats_yearly(lag_df)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    for station_id in stations:
        yearly_stats_slice = yearly_stats[yearly_stats['StageStation'] == station_id]
        ax.plot(yearly_stats_slice['Year'], yearly_stats_slice['mean'], '-', label=station_id)

    ax.legend()
    #ax.set_ylim(bottom=0)
    plt.show()


def plot_monthly_avgs(lag_df, stations):
    monthly_stats = lavg.lag_stats_monthly(lag_df)

    monthly_stats.sort_values(by=['Year', 'Month'], inplace=True)
    monthly_stats['StageTime'] = pd.to_datetime(monthly_stats[['Year', 'Month']].assign(DAY=1))

    fig, ax = plt.subplots(figsize=(14, 8))
    for station_id in stations:
        monthly_means_slice = monthly_stats[monthly_stats['StageStation'] == station_id]
        ax.plot(monthly_means_slice['StageTime'], monthly_means_slice['mean'], '-', label=station_id)

    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
from matplotlib import pyplot as plt
import context
import pandas as pd
import lag_averages as lavg
import hydro_utils as hutils

tableau_colors = ['#4e79a7', '#f28e2c', '#e15759', '#76b7b2', '#59a14f',
                  '#edc949', '#af7aa1', '#ff9da7', '#9c755f', '#bab0ab']

colorblind_palette = ['#0173b2', '#de8f05', '#029e73', '#d55e00', 
                      '#cc78bc', '#ca9161', '#fbafe4', '#949494', '#ece133', '#56b4e9']

hex_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
          '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

normal_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']

color_pallette = tableau_colors

stations = ['CNT', 'PEL', 'CDL', 'GRM', 'CHI', 'CQA', 'CHR', 'CAN']

color_map = {stations[i]: color_pallette[i] for i in range(len(stations))}


def main():
    peaks_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\norm_lag.csv'
    peaks_df = hutils.read_peaks_data(peaks_path)
    lag_df = lavg.make_lag_df(peaks_df)

    lag_df = lag_df[lag_df['StageTime']> '2014-12-30']

    stations = lag_df['StageStation'].unique().tolist()
    print(stations)
    #stations = ['CNT', 'CHR', 'PEL', 'CDL']

    plot_full_avgs(lag_df, stations)
    #plot_yearly_avgs(lag_df, stations)
    #plot_monthly_avgs(lag_df, stations)


def plot_full_avgs(lag_df, stations):
    # Import font management
    import matplotlib.font_manager as fm
    
    # Set Roboto Mono as the font family
    plt.rcParams['font.family'] = 'Bahnschrift'
    
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
        ax.bar(station_stats['StageStation'], station_stats['mean'], 
                label=sorted_stations[i], color=color_pallette[0])#color_map[sorted_stations[i]])

    # Set title and axis labels with the font
    ax.set_title('Average Lag Time by Station', fontsize=16)
    ax.set_xlabel('Station', fontsize=14)
    ax.set_ylabel('Mean Lag Time (hours)', fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Apply font to tick labels
    """for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontname('Agency FB')"""
    
    # Create and style the legend
    #legend = ax.legend()
    
    plt.tight_layout()
    plt.show()

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
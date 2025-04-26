from matplotlib import pyplot as plt
import pandas as pd
import numpy as np


def main():
    peaks_path = r'Data\hydro\lag_data\norm_lag.csv'
    peaks_df = pd.read_csv(peaks_path, parse_dates=['StageTime', 'PrecipTime'])
    
    for station_id in peaks_df['StageStation'].unique():
        plot_lag_dist(peaks_df, station_id)
        plot_lag_dist(peaks_df[peaks_df['PrecipValue']>10], station_id)


def plot_lag_dist(peaks_df, station_id):
    """
    Plot the distribution of lag times.

    Args:
        lag_df (pd.DataFrame): DataFrame containing lag data.
        station_id (str): Station ID to be used in the plot title.
    """
    
    lag_df = peaks_df[peaks_df['StageStation']==station_id].copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h') #convert to hours

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.hist(lag_df['Lag'], bins=[0,1,2,3,4,5,6,7,8,9,10,11,12], color='blue', alpha=0.7)
    ax.set_xlabel('Lag Time (hours)')
    ax.set_ylabel('Frequency')
    ax.set_title(f'Lag Time Distribution at {station_id}')
    plt.show()


def plot_precip_vs_lag(peaks_df, station_id):
    """
    Precip vs lag. Not very compelling.

    Args:
        lag_df (pd.DataFrame): DataFrame containing lag data.
        station_id (str): Station ID to be used in the plot title.
    """
    
    lag_df = peaks_df[peaks_df['StageStation']==station_id].copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h') #convert to hours

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(lag_df['PrecipValue'], lag_df['Lag'], '.r')
    ax.set_xlabel('Precipitation (mm)')
    ax.set_ylabel('Lag Time (hours)')
    ax.set_title(f'Lag Time Distribution at {station_id}')
    plt.show()



if __name__ == '__main__':
    main()
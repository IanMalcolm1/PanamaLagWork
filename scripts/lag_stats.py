"""
Functions for making tables of average lag time over different time periods.
"""

import pandas as pd
import numpy as np
import hydro_utils as hutils


def main():
    lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'
    full_stats_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_stats_full.csv'
    
    peaks_df = hutils.read_peaks_data(lagpath)
    lag_df = make_lag_df(peaks_df)

    stats_full = lag_stats_full(lag_df)
    print(stats_full)
    yearly_means = lag_stats_yearly(lag_df)
    print(yearly_means)
    monthly_means = lag_stats_monthly(lag_df)

    stats_full.to_csv(full_stats_path, index=False)


def make_lag_df(peaks_df):
    """
    Create a DataFrame with lag times for each station.
    
    Args:
        peaks_df (pd.DataFrame): DataFrame containing peak data.
    
    Returns:
        pd.DataFrame: DataFrame with lag times for each station.
    """
    lag_df = peaks_df.copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h')  # convert to hours
    return lag_df


def lag_stats_full(lag_df):
    """
    Calculate the average lag time for each station for all years.
    """

    lag_gb = lag_df.groupby([lag_df['StageStation']])
    return  lag_gb['Lag'].describe().reset_index()


def lag_stats_yearly(lag_df):
    """
    Calculate the average lag time for each station for each year.
    """
    lag_gb = lag_df.groupby([lag_df['StageTime'].dt.year.rename('Year'), lag_df['StageStation']])
    return lag_gb['Lag'].describe().reset_index()
    

def lag_stats_monthly(lag_df: pd.DataFrame):
    """
    Calculate the average lag time for each station for each month.
    """ 
    lag_df = lag_df.copy()
    lag_df['Year'] = lag_df['StageTime'].dt.year
    lag_df['Month'] = lag_df['StageTime'].dt.month
    lag_gb = lag_df.groupby([lag_df['Year'], lag_df['Month'], lag_df['StageStation']])

    return lag_gb['Lag'].describe().reset_index()


if __name__ == '__main__':
    main()
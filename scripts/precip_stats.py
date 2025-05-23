"""
Functions for making tables of average lag time over different time periods.
"""

import pandas as pd
import numpy as np
import hydro_utils as hutils
from station_id_pairs import STATION_ID_PAIRS_REVERSE
import datetime as dt


def main():
    precip_path = r'Data\hydro\precip_data\precip_15min.csv'
    stats_path = r'Data\hydro\precip_data\precip_stats_full.csv'

    precip_df = hutils.read_precip_data(precip_path, single_time_col=False)
    
    precip_sum_full_df = calc_total_precip(precip_df)
    precip_sum_full_df['Station Code'] = precip_sum_full_df['Station Code'].map(STATION_ID_PAIRS_REVERSE)
    precip_sum_full_df.to_csv(stats_path, index=False)
    print(precip_sum_full_df)

    precip_sum_yearly_df = calc_yearly_precip(precip_df)
    print(precip_sum_yearly_df)


def calc_total_precip(precip_df):
    """
    Calculate the precipitation statistics time for each station for the entire time period.
    """
    precip_station_gb = precip_df.groupby(precip_df['Station Code'])
    precip_sum = precip_station_gb['Value'].sum().reset_index().rename(columns={'Value': 'PrecipSum'})

    return precip_sum


def calc_yearly_precip(precip_df):
    """
    Calculate the precipitation statistics time for each station for each year. Ignores the current year.
    """
    precip_df = precip_df[precip_df['Time'].dt.year < curr_year()]
    precip_gb = precip_df.groupby([precip_df['Time'].dt.year.rename('Year'), precip_df['Station Code']])
    print(precip_gb)
    precip_sum = precip_gb['Value'].sum().reset_index().rename(columns={'Value': 'PrecipSum'})

    return precip_sum


def calc_avg_yearly_precip(precip_df):
    """
    Calculate the average yearly sum of precipitation for each station.
    """
    yearly_precip_df = calc_yearly_precip(precip_df)
    yearly_precip_gb = yearly_precip_df.groupby(yearly_precip_df['Station Code'])
    avg_yearly_precip_df = yearly_precip_gb['PrecipSum'].mean().reset_index().rename(columns={'PrecipSum': 'AvgYearlyPrecipSum'})

    return avg_yearly_precip_df


def curr_year():
    return dt.datetime.now().year
    


if __name__ == '__main__':
    main()
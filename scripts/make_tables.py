import pandas as pd
import numpy as np


def main():
    lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\norm_lag.csv'
    lag_df = pd.read_csv(lagpath, parse_dates=['StageTime', 'PrecipTime'])
    full_averages = average_lag_table(lag_df)
    yearly_means = average_lag_table_yearly(lag_df)
    #monthly_means = average_lag_table_monthly(lag_df)

    print(full_averages)
    print(yearly_means)
    print(monthly_means)


def average_lag_table(peaks_df):
    lag_df = peaks_df.copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h')  # convert to hours

    lag_gb = lag_df.groupby([lag_df['StageStation']])
    yearly_means = lag_gb['Lag'].mean()
    yearly_means = yearly_means.reset_index()

    return yearly_means

def average_lag_table_yearly(peaks_df):
    lag_df = peaks_df.copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h')  # convert to hours

    lag_gb = lag_df.groupby([lag_df['StageTime'].dt.year.rename('year'), lag_df['StageStation']])
    yearly_means = lag_gb['Lag'].mean()
    yearly_means = yearly_means.reset_index()

    return yearly_means
    
def average_lag_table_monthly(peaks_df):
    lag_df = peaks_df.copy()
    lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
    lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h')  # convert to hours

    lag_df['Date'] = pd.to_datetime([lag_df['StageTime'].dt.year, lag_df['StageTime'].dt.month, 1])

    lag_gb = lag_df.groupby([lag_df['Date'], lag_df['StageStation']])
    yearly_means = lag_gb['Lag'].mean()
    yearly_means = yearly_means.reset_index()

    return yearly_means


if __name__ == '__main__':
    main()
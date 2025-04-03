import pandas as pd

def get_data(
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_hourly.csv',
    stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly.csv',
    date_cols = ['Start of Interval (UTC)', 'End of Interval (UTC)'],
    time_col = 'End of Interval (UTC)'
):
    """Reads in the data files and returns the dataframes."""

    precip_df = pd.read_csv(precip_path, parse_dates=date_cols)
    stage_df = pd.read_csv(stage_path, parse_dates=date_cols)

    rename_cols = {
        time_col: 'Time',
    }

    precip_df.rename(columns=rename_cols, inplace=True)
    stage_df.rename(columns=rename_cols, inplace=True)

    return precip_df, stage_df
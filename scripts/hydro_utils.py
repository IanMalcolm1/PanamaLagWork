import pandas as pd


def range_mask(
        df: pd.DataFrame,
        station_code: str,
        start_datetime: str, end_datetime: str,
        time_col='Time', station_col='Station Code') -> pd.Series:
    """
    Makes a mask for a given station and time period.
    Args:
        df: DataFrame containing the data
        station_code: Station code to filter by
        start_datetime: Start datetime string in 'YYYY-MM-DD HH:MM:SS' format
        end_datetime: End datetime string in 'YYYY-MM-DD HH:MM:SS'
        time_col: Column name for the time data (default is 'Time')
        station_col: Column name for the station code (default is 'Station Code')
    """
    start_date = pd.to_datetime(start_datetime)
    end_date = pd.to_datetime(end_datetime)
    print(start_date, end_date)

    return (df[station_col] == station_code) & (df[time_col] >= start_date) & (df[time_col] <= end_date)


def read_longitudinal_data(
    table_path: str,
    date_cols: list[str],
    drop_cols: list[str] | None,
    rename_cols: dict[str,str] | None,
):
    """Handles the date columns in the original data. Applies rename and drop operations."""

    df = pd.read_csv(table_path, parse_dates=date_cols)

    if drop_cols is not None:
        df = df.drop(columns=drop_cols)
    
    if rename_cols is not None:
        df = df.rename(columns=rename_cols)

    return df


def read_stage_data_og(stage_path):
    """Wrapper around read_longitudinal_data()."""
    stage_df = read_longitudinal_data(
        stage_path,
        date_cols = ['Start of Interval (UTC)', 'End of Interval (UTC)'],
        drop_cols = ['Start of Interval (UTC)'],
        rename_cols = {'End of Interval (UTC)': 'Time'}
    )

    return stage_df


def read_stage_data_norm(stage_path):
    """Wrapper around read_longitudinal_data()."""
    stage_df = read_longitudinal_data(
        stage_path,
        date_cols = ['Time'],
        drop_cols = None,
        rename_cols = {'End of Interval (UTC)': 'Time'}
    )

    return stage_df


def read_precip_data(precip_path):
    """Wrapper around read_longitudinal_data()."""
    precip_df = read_longitudinal_data(
        precip_path,
        date_cols = ['Start of Interval (UTC)', 'End of Interval (UTC)'],
        drop_cols = ['Start of Interval (UTC)'],
        rename_cols = {'End of Interval (UTC)': 'Time'}
    )

    return precip_df


def read_lag_data(lag_path):
    """Wrapper around read_longitudinal_data()."""
    lag_df = read_longitudinal_data(
        lag_path,
        date_cols = ['StageTime', 'PrecipTime'],
        drop_cols = None,
        rename_cols = None
    )

    return lag_df
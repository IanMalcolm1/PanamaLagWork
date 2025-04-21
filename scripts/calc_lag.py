import pandas as pd
import scipy.signal as sig
import numpy as np
import hydro_utils


def main():
    """
    Runs associate_peaks for rainy season of each year, and concatenate results.
    """    
    # Data paths
    precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_15min.csv'
    stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par_norm.csv'
    out_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\lag_15min.csv'

    # Input data
    precip_df = hydro_utils.read_precip_data(precip_path, single_time_col=False)
    stage_df = hydro_utils.read_stage_data_norm(stage_path)

    # List of station ID pairs (index 0 is river station, 1 is precip station)
    station_id_pairs = [
        ['CNT', 'CNT'],
        ['PEL', 'PEL'],
        ['CDL', 'CDL'],
        ['GRM', 'ARC'],
        ['CHI', 'CHI'],
        ['CQA', 'ZAN'],
        ['CHR', 'CHR'],
        ['CAN', 'CAN'],
    ]

    # Specific arguments for each station
    stage_peaks_args_map = {
        'CNT': {'prominence': 0.75, 'distance': 2},
        'PEL': {'prominence': 0.75, 'distance': 2},
        'CDL': {'prominence': 0.75, 'distance': 2},
        'GRM': {'prominence': 0.75, 'distance': 2},
        'CHI': {'prominence': 0.75, 'distance': 2},
        'CQA': {'prominence': 0.75, 'distance': 2},
        'CHR': {'prominence': 0.75, 'distance': 2},
        'CAN': {'prominence': 0.75, 'distance': 2},
    }

    # Run calculations
    peak_dfs = []
    for station_id_pair in station_id_pairs:
        stage_station_id = station_id_pair[0]
        precip_station_id = station_id_pair[1]

        peaks_df = associate_peaks_full(
            stage_df=stage_df,
            precip_df=precip_df,
            stage_station=stage_station_id,
            precip_station=precip_station_id,
            year_span=(2000, 2024),
            month_span=(5, 1), #rainy season only
            stage_peaks_args=stage_peaks_args_map[stage_station_id],
            max_distance=12,
            min_precip=2
        )

        peak_dfs.append(peaks_df)
    
    # Concatenate all results into a single DataFrame
    full_df = pd.concat(peak_dfs, ignore_index=True)
    full_df.dropna(subset=['PrecipTime'], inplace=True)

    # Save 
    full_df.to_csv(out_path, index=False)


def associate_peaks_full(stage_df: pd.DataFrame, precip_df: pd.DataFrame,
                         stage_station: str,
                         year_span: tuple[pd.Timestamp, pd.Timestamp],
                         precip_station: str = None,
                         month_span: tuple[int, int] = None,
                         stage_peaks_args: dict = {'prominence': 0.25, 'distance': 4},
                         max_distance: int = 6, min_precip=1) -> pd.DataFrame:
    """
    Associates rainfall and stage peaks for multiple years. Calls associate_peaks
    for each year in the year_span range, for each month in the month_span range.
    Concatentates results to a single dataframe.

    Args:
        stage_df (pandas.DataFrame): The stage data. Must include 'Time',
            'Station Code', and 'Value' columns.
        precip_df (pandas.DataFrame): The precipitation data. Must include
            'Time', 'Station Code', and 'Value' columns.
        stage_station (str): The 3-letter station code for the stage station
        year_span (tuple[pandas.Timestamp, pandas.Timestamp]): The start and end years
            for the analysis. Ensure good data coverage is present for specified years.
        precip_station (str): The 3-letter station code for the precipitation station
            (if None, set to same as stage_station)
        month_span (tuple[int, int]): The start and end months for the analysis. This is useful
            for focusing on a specific part of the year, such as the Panama rainy season. If
            None, no month filtering is applied. If the second value is less than or equal to
            the first, the range is assumed to span to the subsequent year.
        stage_peaks_args (dict): Keyword arguments for scipy.signal.find_peaks for
            stage peaks. Default values are prominence=0.1 and distance=4.
        max_distance (int): The maximum number of hours between a stage peak and a
            rainfall peak.
    
    Returns:
        pandas.DataFrame: A DataFrame with columns 'StageTime', 'StageStation', 'StageValue',
            'PrecipTime', 'PrecipStation', and 'PrecipValue'. Rows represent pairs of
            associated peaks.
    """
    if month_span is None:
        month_span = (1, 1)

    peaks_dfs = []
    for year in range(year_span[0], year_span[1]+1):
        #set time span
        if month_span[0] < month_span[1]:
            start_time = pd.Timestamp(f'{year}-{month_span[0]}-01')
            end_time = pd.Timestamp(f'{year}-{month_span[1]}-01')
        else:
            start_time = pd.Timestamp(f'{year}-{month_span[0]}-01')
            end_time = pd.Timestamp(f'{year+1}-{month_span[1]}-01')
        time_span = (start_time, end_time)

        peak_df = associate_peaks(
            stage_df=stage_df,
            precip_df=precip_df,
            stage_station=stage_station,
            precip_station=precip_station,
            time_span=time_span,
            stage_peaks_args=stage_peaks_args,
            max_distance=max_distance,
            min_precip=min_precip
        )

        peaks_dfs.append(peak_df)

    return pd.concat(peaks_dfs, ignore_index=True)


def associate_peaks(stage_df: pd.DataFrame, precip_df: pd.DataFrame,
                    stage_station: str, precip_station: str = None,
                    time_span: tuple[pd.Timestamp, pd.Timestamp] = None,
                    stage_peaks_args: dict = {'prominence': 0.25, 'distance': 4},
                    max_distance: int = 6, min_precip=1) -> pd.DataFrame:
    """
    Associates rainfall and stage peaks. Finds stage peaks using scipy.signal.find_peaks,
    then finds the largest rainfall peak within a specified time window before each stage peak.
    
    Args:
        stage_df (pandas.DataFrame): The stage data. Must include 'Time',
            'Station Code', and 'Value' columns.
        precip_df (pandas.DataFrame): The precipitation data. Must include
            'Time', 'Station Code', and 'Value' columns.
        stage_station (str): The 3-letter station code for the stage station
        precip_station (str): The 3-letter station code for the precipitation station
            (if None, set to same as stage_station)
        time_span (tuple[pandas.Timestamp, pandas.Timestamp]): The start and end dates
            for the analysis. If None, no date filtering is applied.
        stage_peaks_args (dict): Keyword arguments for scipy.signal.find_peaks for
            stage peaks. Default values are prominence=0.1 and distance=4.
        max_distance (int): The maximum number of hours between a stage peak and a
            rainfall peak.
        min_precip (float): The minimum precipitation value needed to be considered a peak.
    
    Returns:
        pandas.DataFrame: A DataFrame with columns 'StageTime', 'StageStation', 'StageValue',
            'PrecipTime', 'PrecipStation', and 'PrecipValue'. Rows represent pairs of
            associated peaks.
    """
    print(f"Associating {stage_station} stage peaks with {precip_station} rainfall peaks for {time_span}")
    
    # Columns mask
    clip_stage_df = stage_df[['Time', 'Station Code', 'Value']]
    clip_precip_df = precip_df[['Time', 'Station Code', 'Value']]

    # Stations mask
    if precip_station is None:
        precip_station = stage_station

    clip_stage_df = clip_stage_df[clip_stage_df['Station Code'] == stage_station]
    clip_precip_df = clip_precip_df[clip_precip_df['Station Code'] == precip_station]

    # Time mask
    if time_span is not None:
        precip_mask = (clip_precip_df['Time'] >= time_span[0]) & (clip_precip_df['Time'] <= time_span[1])
        clip_precip_df = clip_precip_df[precip_mask]

        stage_mask = (clip_stage_df['Time'] >= time_span[0]) & (clip_stage_df['Time'] <= time_span[1])
        clip_stage_df = clip_stage_df[stage_mask]

    # Find stage peaks
    stage_peak_idxs, _ = sig.find_peaks(clip_stage_df['Value'], **stage_peaks_args)

    # Make new df with only peaks
    stage_peaks_df: pd.DataFrame = clip_stage_df.iloc[stage_peak_idxs]

    # Also slice columns
    stage_peaks_df = stage_peaks_df[['Time', 'Station Code', 'Value']].copy(deep=True)
    stage_peaks_df = stage_peaks_df.reset_index(drop=True)

    # Add column to stage peaks df for time of associated rainfall peaks
    stage_peaks_df['PrecipTime'] = np.full(stage_peaks_df.shape[0], np.nan, dtype='datetime64[ns]')

    # Rename columns
    rename_cols  = {
        'Time': 'StageTime',
        'Station Code': 'StageStation',
        'Value': 'StageValue'
    }
    stage_peaks_df.rename(columns=rename_cols, inplace=True)

    # Find associated rainfall peaks
    precip_peak_times = set()
    for row in stage_peaks_df.itertuples():
        stage_time = row.StageTime
        min_time = stage_time - pd.Timedelta(hours=max_distance) #farthest back to search for a peak
        
        # Filter precipitation data to only include values in the time range, and only peaks
        precip_slice = clip_precip_df[(clip_precip_df['Time'] >= min_time) & (clip_precip_df['Time'] <= stage_time)]
        precip_peak_idxs, _ = sig.find_peaks(precip_slice['Value'])
        precip_slice = precip_slice.iloc[precip_peak_idxs]
        precip_peak_time = None

        while not precip_slice.empty and precip_peak_time is None:
            #identify time of largest precip peak in range
            max_idx = precip_slice['Value'].idxmax()
            max_val = precip_slice.at[max_idx, 'Value']
            precip_peak_time = precip_slice.at[max_idx, 'Time']

            # If the precip peak is under some threshold, assume it is invalid and set it to None
            if max_val < min_precip:
                precip_peak_time = None
                break #return early because no other values will be larger

            # Try again if current max already claimed by a previous stage peak
            if precip_peak_time in precip_peak_times:
                # Only search after the claimed precip peak
                precip_slice = precip_slice[precip_slice['Time'] > precip_peak_time]
                precip_peak_time = None #essentially continue loop
    
        stage_peaks_df.at[row.Index, 'PrecipTime'] = precip_peak_time
        precip_peak_times.add(precip_peak_time)

    # Drop rows with no associated rainfall peaks
    # This is generally due to a gaps in the precipitation data
    stage_peaks_df.dropna(subset=['PrecipTime'], inplace=True)
    print(f"No precipitation peak found for {len(stage_peak_idxs)-stage_peaks_df.shape[0]} stage peaks")
    print()

    # Join with precipitation data
    full_peaks_df = pd.merge(
        left=stage_peaks_df,
        right=clip_precip_df,
        left_on='PrecipTime',
        right_on='Time',
        how='left'
    )

    # Clean final dataframe
    full_peaks_df.drop(columns=['Time'], inplace=True)
    rename_cols = {
        'Station Code': 'PrecipStation',
        'Value': 'PrecipValue'
    }
    full_peaks_df.rename(columns=rename_cols, inplace=True)
    
    return full_peaks_df


if __name__ == '__main__':
    main()
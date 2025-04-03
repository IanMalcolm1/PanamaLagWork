"""
This script helps clean up data taken from the Panama Canal Authority's data website.
"""

import pandas as pd
import os

def fix_cols(base_path):
    stage_cols_df = pd.read_csv(base_path, header=1, nrows=10) #just get column rows (10 rows is more than enough)

    station_ids = list(stage_cols_df.columns) #this should be 2 'Unnamed: n' columns, then the station ids
    data_types = list(stage_cols_df.iloc[1]) #this should be 2 NaNs and then sensor names
    data_units = list(stage_cols_df.iloc[2]) #this should be 2 'Start/End of Interval' cols and then data type/units

    new_cols = []
    for i in range(len(station_ids)):
        if not station_ids[i].startswith('Unnamed'):
            new_cols.append(f"{station_ids[i]}\t{data_types[i]}\t{data_units[i]}")
        else:
            new_cols.append(data_units[i])

    base_df = pd.read_csv(base_path, header=4)
    base_df.columns = new_cols

    melt_df = base_df.melt(id_vars=new_cols[:2], value_name='Value')

    melt_df = melt_df.dropna(subset=['Value'])

    melt_df[['Station Code', 'Sensor', 'Data Type']] = melt_df['variable'].str.split('\t', expand=True)

    melt_cols = melt_df.columns.tolist()
    melt_cols.remove('variable')
    melt_cols.append(melt_cols.pop(2))
    melt_df = melt_df[melt_cols]

    return melt_df


def prep_singular(inpath, outpath):
    """Preps and saves a single file"""
    melt_df = fix_cols(inpath)

    melt_df.to_csv(outpath, index=False)


def prep_and_merge(indir, outpath):
    """
    Preps and combines all csv files in a directory into a single file. This is useful when the PCA website
    can't handle a full data export, and you have to split the data into a series of smaller time periods.
    
    Args:
        indir (str): The directory containing the csv files
        outpath (str): The path to save the merged csv file
    """

    for _, _, files in os.walk(indir):
        break

    melt_dfs = []
    for file in files:
        if file.endswith('.csv'):
            csv_path = os.path.join(indir, file)
            melt_dfs.append (fix_cols(csv_path))

    concat_df = pd.concat(melt_dfs)

    concat_df.to_csv(outpath, index=False)



if __name__=='__main__':
    indir = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\StationData\precip_raw'
    outpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\StationData\precip_hourly_melt.csv'

    prep_and_merge(indir, outpath)

    

    
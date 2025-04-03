import pandas as pd
import sklearn.preprocessing as sklp
import hydro_utils
import numpy as np

def main():
    _, stage_df = hydro_utils.get_data()

    stage_norm_df = normalize_rivers(stage_df)
    opath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly_normalized.csv'
    stage_norm_df.to_csv(opath, index=False)


def normalize_rivers(stage_df: pd.DataFrame):
    """
    Normalize the stage data for each river
    """
    rivers = stage_df['Station Code'].unique()
    river_dbs = []
    for river in rivers:
        river_df: pd.DataFrame = stage_df[stage_df['Station Code'] == river]
        river_mean = river_df['Value'].mean()
        river_std = river_df['Value'].std()
        river_df['Value'] = (river_df['Value']-river_mean)/river_std
        
        river_dbs.append(river_df)

    norm_df = pd.concat(river_dbs, ignore_index=True)
    return norm_df


if __name__ == '__main__':
    main()
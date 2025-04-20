from matplotlib import pyplot as plt
import pandas as pd
import hydro_utils

def main():
    # Data paths
    og_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par.csv'
    out_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par_norm.csv'

    stage_df = hydro_utils.read_stage_data_og(og_path)

    stage_df = remove_stage_outliers(stage_df)
    stage_norm_df = normalize_rivers(stage_df)

    stage_norm_df.to_csv(out_path, index=False)


def normalize_rivers(stage_df: pd.DataFrame):
    """
    Normalize the stage data for each river
    """
    rivers = stage_df['Station Code'].unique()
    river_dbs = []
    for river in rivers:
        river_df: pd.DataFrame = stage_df[stage_df['Station Code'] == river].copy()
        river_mean = river_df['Value'].mean()
        river_std = river_df['Value'].std()
        test_column = (river_df['Value']-river_mean)/river_std
        river_df['Value'] = test_column

        print(f"Station: {river} - Mean: {river_mean:.2f} - Std: {river_std:.2f}")
        
        river_dbs.append(river_df)

    norm_df = pd.concat(river_dbs, ignore_index=True)
    return norm_df


_outlier_mask_data = [
    ['CNT', '2017-09-23 15:00:00', '2018-02-15'],
    ['CNT', '2018-08-18', '2018-08-23'],
    ['CHR', '2017-07-05 23:00:00', '2019-01-19'], #has a long string of weird spikes and some huge outliers
    #['CHR', '2018-09-10 18:00:00', '2018-09-12'],
    #['CHR', '2018-11-17', '2018-12-05'],
    ['CDL', '2015-11-24', '2015-12-03'],
    ['GRM', '2017-09-29 16:00:00', '2017-09-29 17:00:00'],
    ['GRM', '2017-11-05 06:00:00', '2017-11-07'],
    ['GRM', '2017-11-25 22:00:00', '2017-11-26 02:00:00'],
    ['GRM', '2018-01-27 12:00:00', '2018-01-27 16:00:00'],
    ['GRM', '2018-08-22', '2018-08-24 15:00:00'],
    ['GRM', '2018-08-27 12:00:00', '2018-08-28'],
    ['GRM', '2018-09-30 16:00:00', '2018-09-30 18:00:00'],
    ['GRM', '2018-10-18 21:47:00', '2018-10-18 21:48:20'],
    ['GRM', '2018-11-19', '2018-11-29 08:00:00'],
    #['GRM', '2018-11-21 03:00:00', '2018-11-21 12:00:00'],
    #['GRM', '2018-11-26', '2018-11-26 12:00:00'],
    #['GRM', '2018-11-28 20:00:00', '2018-11-29 04:00:00'],
    ['GRM', '2019-01-22', '2019-03-22'],
    ['GRM', '2019-06-12 06:00:00', '2019-06-12 20:00:00'],
]


def remove_stage_outliers(stage_df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes outliers in the stage data.
    """
    mega_mask = hydro_utils.range_mask(stage_df, *_outlier_mask_data[0])
    for mask_data in _outlier_mask_data[1:]:
        mask = hydro_utils.range_mask(stage_df, *mask_data)
        mega_mask = mega_mask | mask
    
    return stage_df[~mega_mask]

def vis_outliers(stage_df):
    stations = stage_df['Station Code'].unique().tolist()

    # Plot all data
    for station in stations:
        fig, ax = plt.subplots(figsize=(14, 8))
        station_df = stage_df[stage_df['Station Code'] == station]
        ax.plot(station_df['Time'], station_df['Value'], label=station)

        for mask_data in _outlier_mask_data:
            if mask_data[0] == station:
                mask = hydro_utils.range_mask(station_df, *mask_data)
                mask_df = station_df[mask]
                ax.plot(mask_df['Time'], mask_df['Value'], color='black', linewidth=2)

        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized Stage')
        ax.legend()
        plt.show()
        plt.close()

    # Plot all data
        fig, ax = plt.subplots(figsize=(14, 8))
        station_df = stage_df[stage_df['Station Code'] == station]
        mega_mask = hydro_utils.range_mask(station_df, 'GRM', '2018-11-26', '2018-11-28')

        for mask_data in _outlier_mask_data:
            if mask_data[0] == station:
                if mega_mask is None:
                    mega_mask = hydro_utils.range_mask(station_df, *mask_data)
                else:
                    mega_mask = mega_mask | hydro_utils.range_mask(station_df, *mask_data)
                mask = hydro_utils.range_mask(station_df, *mask_data)
                
        mask_df = station_df[~mega_mask]
        ax.plot(mask_df['Time'], mask_df['Value'], label=station)

        ax.set_xlabel('Date')
        ax.set_ylabel('Normalized Stage')
        ax.legend()
        plt.show()
        plt.close()
    

if __name__ == '__main__':
    main()
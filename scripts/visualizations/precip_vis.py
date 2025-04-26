import pandas as pd
from matplotlib import pyplot as plt
import context
import hydro_utils as hutils

def main():
    precip_path = r'Data\hydro\precip_data\precip_15min.csv'
    stage_path = r'Data\hydro\stage_data\river_stage_par.csv'

    precip_df = hutils.read_precip_data(precip_path, single_time_col=False)
    stage_df = hutils.read_stage_data_og(stage_path)

    stations = ['CHI', 'ZAN', 'GAD']
    stations = ['CNT', 'PEL', 'CDL', 'ARC', 'CHI', 'ZAN', 'CHR', 'GAD']
    stations = ['CAN']


    fig, ax = plt.subplots(figsize=(14, 8))
    for station_id in stations:
        yearly_slice = precip_df[(precip_df['Time'].dt.year == 2020) & (precip_df['Station Code'] == station_id)]
        ax.plot(yearly_slice['Time'], yearly_slice['Value'], label=station_id)


    ax.legend()
    plt.show()

    for station_id in stations:
        yearly_slice = precip_df[(precip_df['Station Code'] == station_id)]
        print(f"Avg precip for {station_id}: {yearly_slice['Value'].mean()}\nStd: {yearly_slice['Value'].std()}\n")

        stage_yearly_slice = stage_df[(stage_df['Time'].dt.year > 2019) & (stage_df['Station Code'] == station_id)]
        print(f"Avg stage for {station_id}: {stage_yearly_slice['Value'].mean()}\nStd: {stage_yearly_slice['Value'].std()}\n")

        print(f"Time range for {station_id}: {yearly_slice['Time'].min()} to {yearly_slice['Time'].max()}\n")



if __name__ == '__main__':
    main()
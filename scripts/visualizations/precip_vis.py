import pandas as pd
from matplotlib import pyplot as plt

def main():
    precip_df, stage_df = get_data()

    stations = ['CNT', 'PEL', 'CDL']

    fig, ax = plt.subplots(figsize=(14, 8))
    for station_id in stations:
        yearly_slice = precip_df[(precip_df['Time'].dt.year == 2020) & (precip_df['Station Code'] == station_id)]
        ax.plot(yearly_slice['Time'], yearly_slice['Value'], '-', label=station_id)

    ax.legend()
    plt.show()

    for station_id in stations:
        yearly_slice = precip_df[(precip_df['Time'].dt.year > 2019) & (precip_df['Station Code'] == station_id)]
        print(f"Avg precip for {station_id}: {yearly_slice['Value'].mean()}\nStd: {yearly_slice['Value'].std()}\n")

        stage_yearly_slice = stage_df[(stage_df['Time'].dt.year > 2019) & (stage_df['Station Code'] == station_id)]
        print(f"Avg stage for {station_id}: {stage_yearly_slice['Value'].mean()}\nStd: {stage_yearly_slice['Value'].std()}\n")


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


if __name__ == '__main__':
    main()
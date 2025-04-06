from matplotlib import pyplot as plt
import context
import hydro_utils


PLOT_NORM = False


def main():
    # Data paths
    norm_stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly_norm.csv'
    og_stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_hourly.csv'

    # Read data
    if PLOT_NORM:
        stage_df = hydro_utils.read_stage_data_norm(norm_stage_path)
    else:
        stage_df = hydro_utils.read_stage_data_og(og_stage_path)

    plot_stage(stage_df)



def plot_stage(stage_df):
    stations = stage_df['Station Code'].unique().tolist()

    # Plot all data
    fig, ax = plt.subplots(figsize=(14, 8))
    for station in stations:
        station_df = stage_df[stage_df['Station Code'] == station]
        ax.plot(station_df['Time'], station_df['Value'], label=station)

    ax.set_xlabel('Date')
    ax.set_ylabel('Normalized Stage')
    ax.legend()
    plt.show()
    plt.close()


if __name__=='__main__':
    main()
import context
import lag_stats, precip_stats as precip_stats, hydro_utils as hutils
import matplotlib.pyplot as plt
from colors import LAG_COLOR_MAP
from station_id_pairs import STATION_ID_PAIRS_REVERSE

precip_path = r'Data\hydro\precip_data\precip_15min.csv'

precip_df = hutils.read_precip_data(precip_path, single_time_col=False)

precip_sums_df = precip_stats.calc_total_precip(precip_df).sort_values(by=['PrecipSum'], ascending=False)

precip_sums_df['Station Code'] = precip_sums_df['Station Code'].map(STATION_ID_PAIRS_REVERSE)

stations = precip_sums_df['Station Code'].unique().tolist()

fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(precip_sums_df['Station Code'], precip_sums_df['PrecipSum'], label="Average Precipitation")

for i in range(len(stations)):
    station_stats = precip_sums_df[precip_sums_df['Station Code'] == stations[i]]
    ax.bar(
        station_stats['Station Code'], station_stats['PrecipSum'],
        color=LAG_COLOR_MAP[stations[i]], edgecolor='black',
        label=stations[i]
    )

# Add title and axis labels
ax.set_title('Total Precipitation by Station')
ax.set_xlabel('Station')
ax.set_ylabel('Total Precipitation (mm)')

plt.tight_layout()
plt.show()
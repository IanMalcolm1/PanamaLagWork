import context
import lag_stats, precip_sums, hydro_utils as hutils
import matplotlib.pyplot as plt

precip_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\precip_data\precip_15min.csv'

precip_df = hutils.read_precip_data(precip_path, single_time_col=False)

precip_sums_df = precip_sums.precip_sum_full(precip_df)

fig, ax = plt.subplots(figsize=(14, 8))
ax.bar(precip_sums_df['Station Code'], precip_sums_df['PrecipSum'], label="Average Precipitation")

plt.show()
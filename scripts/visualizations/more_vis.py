import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

lagpath = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\lag_data\norm_lag.csv'
lag_df = pd.read_csv(lagpath, parse_dates=['StageTime', 'PrecipTime'])

lag_df['Lag'] = lag_df['StageTime'] - lag_df['PrecipTime']
lag_df['Lag'] = lag_df['Lag'] / np.timedelta64(1, 'h') #convert to hours

lag_gb = lag_df.groupby([lag_df['StageTime'].dt.year.rename('year'), lag_df['StageTime'].dt.month.rename('month'), lag_df['StageStation']])
yearly_means = lag_gb['Lag'].mean()
yearly_means = yearly_means.reset_index()
yearly_means['date'] = pd.to_datetime(yearly_means[['year', 'month']].assign(day=1))
yearly_means

type(yearly_means)
print(yearly_means.index)
stations = lag_df['StageStation'].unique().tolist()
stations


fig, ax = plt.subplots(figsize=(14, 8))
for station_id in stations:
    yearly_means_slice = yearly_means[yearly_means['StageStation'] == station_id]
    ax.plot(yearly_means_slice['date'], yearly_means_slice['Lag'], '-', label=station_id)

ax.legend()
plt.show()
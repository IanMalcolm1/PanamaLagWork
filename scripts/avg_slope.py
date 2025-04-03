import os
import pandas as pd


def main():
    profiles_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\elevation_profiles'
    for _,_,filenames in os.walk(profiles_path):
        break

    for filename in filenames:
        if filename.endswith('.csv'):
            filepath = os.path.join(profiles_path, filename)
            df = pd.read_csv(filepath)

            min_idx = df['Distance'].idxmin()
            max_idx = df['Distance'].idxmax()

            min_dist = df.at[min_idx, 'Distance']
            max_dist = df.at[max_idx, 'Distance']

            print(min_dist, max_dist)

            min_elev = df.at[min_idx, 'Elevation']
            max_elev = df.at[max_idx, 'Elevation']

            print(f'Average percent slope for {filename} is {((max_elev - min_elev) / (max_dist - min_dist))*100}')


if __name__ == '__main__':
    main()
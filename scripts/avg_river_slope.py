import os
import pandas as pd


def main():
    profiles_path = r'Data\hydro\elevation_profiles'
    outname = "river_slopes.csv"
    outpath = rf'Data\hydro\elevation_profiles\{outname}'

    for _,_,filenames in os.walk(profiles_path):
        break

    slopes = []
    for filename in filenames:
        if filename.endswith('.csv') and filename != outname:
            filepath = os.path.join(profiles_path, filename)
            df = pd.read_csv(filepath)

            min_idx = df['Distance'].idxmin()
            max_idx = df['Distance'].idxmax()

            min_dist = df.at[min_idx, 'Distance']
            max_dist = df.at[max_idx, 'Distance']

            print(min_dist, max_dist)

            min_elev = df.at[min_idx, 'Elevation']
            max_elev = df.at[max_idx, 'Elevation']

            slope_percent = abs(((max_elev - min_elev) / (max_dist - min_dist))*100)

            slopes.append({
                'station_id': filename,
                'slope_percent': slope_percent,
                'min_elev': min(min_elev, max_elev),
                'max_elev': max(min_elev, max_elev),
                'distance': max_dist
            })

    slopes_df = pd.DataFrame(slopes)
    slopes_df.to_csv(outpath, index=False)
    print(f"Saved slopes to {outpath}")
    


if __name__ == '__main__':
    main()
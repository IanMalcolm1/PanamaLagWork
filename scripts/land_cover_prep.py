import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


def main():
    zonal_hist_path = r'Data\MiambienteLandCover\watershed_miambiente_zonal_hist.csv'
    zonal_hist_df = pd.read_csv(zonal_hist_path)
    
    transpose_hist_df = transpose_esri_table(zonal_hist_df)

    merged_df = merge_miambente_cols(transpose_hist_df)
    
    landuse_cols = merged_df.columns[1:]

    norm_hist_df = normalize_hist_df(merged_df, landuse_cols)
    norm_hist_df = norm_hist_df.sort_values(by='Forest', ascending=False)

    plot_landcover(norm_hist_df, landuse_cols)

    norm_hist_df.to_csv(r'Data\MiambienteLandCover\miambiente_landuse_merged_groups.csv', index=False)



def transpose_esri_table(df: pd.DataFrame):
    """Transposes the Esri table to a more usable format."""
    out_df = df.transpose()
    out_df.reset_index(inplace=True)
    out_df.rename(lambda x: out_df[x].iloc[0], axis=1, inplace=True)
    out_df.drop(index=0, inplace=True)
    out_df.rename(columns={'LABEL': 'WatershedId'}, inplace=True)
    out_df['WatershedId'] = out_df['WatershedId'].map(lambda x: x[6:])

    landuse_cols = out_df.columns[1:]
    for col in landuse_cols:
        if out_df[col].sum() < 1:
            out_df.drop(columns=col, inplace=True)
        else:
            out_df[col] = out_df[col].astype(int)

    return out_df



def merge_miambente_cols(df: pd.DataFrame):
    """Merges the columns of the dataframe. Removes water column."""
    df = df.copy()

    merge_dict = {
        'Forest': ['Bosque latifoliado mixto maduro', 'Bosque latifoliado mixto secundario',
                   'Bosque plantado de coníferas', 'Bosque plantado de latifoliadas'],
        'Shrubland': ['Rastrojo y vegetación arbustiva'],
        'Pasture/Grassland': ['Vegetación herbácea', 'Pasto'],
        'Crops': ['Café', 'Piña'],
        'Urban/Industrial': ['Área poblada', 'Infraestructura', 'Explotación minera'],
    }

    df = df.drop(columns=['Superficie de agua'])

    for new_col, old_cols in merge_dict.items():
        new_col_data = df[old_cols].sum(axis=1)
        df = df.drop(columns=old_cols)
        df[new_col] = new_col_data

    return df


def normalize_hist_df(hist_df: pd.DataFrame, landuse_cols: list[str]):
    """Normalizes the histogram data to percentages."""
    hist_norm_df = hist_df.copy().reset_index(drop=True)

    sums = hist_norm_df[landuse_cols].sum(axis=1)
    hist_norm_df[landuse_cols] = hist_norm_df[landuse_cols].divide(sums/100, axis=0)

    return hist_norm_df


def plot_landcover(norm_hist_df: pd.DataFrame, landuse_cols: list[str]):
    """Plots the normalized histogram data."""
    fig, ax = plt.subplots(figsize=(14, 8))

    bottom = np.zeros(len(norm_hist_df))
    for col in landuse_cols:
        ax.bar(norm_hist_df['WatershedId'], norm_hist_df[col], bottom=bottom, label=col)
        bottom += norm_hist_df[col].to_numpy()

    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
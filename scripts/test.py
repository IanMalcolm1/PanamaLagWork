import hydro_utils as hutils

stage_path = r'C:\Users\ianma\OneDrive - University of Redlands\GisCapstone\Data\hydro\stage_data\river_stage_par_norm.csv'

stage_df = hutils.read_stage_data_norm(stage_path)

stage_df = stage_df.sort_values(by=['Station Code', 'Time'])

stage_df.to_csv(stage_path, index=False)
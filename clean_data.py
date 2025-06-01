from config import *
from read_xks import *
from format_data import pivot_monthly_dataframe
from utils import manage_station_directory
import numpy as np
import os

def clean_data (df, output_dir, variable):
    df_dropped_years = drop_years_with_min_months(df)
    cleaned_data = nullify_high_z_scores(df_dropped_years, output_dir, variable)
    return cleaned_data

def drop_years_with_min_months(df):
    print(df.shape)
    initial_rows = len(df)
    df = df.dropna(thresh= min_months_per_year + df.shape[1] - 12, axis=0)
    dropped_rows = initial_rows - len(df)
    print(f"Dropped {dropped_rows} rows with less than {min_months_per_year} months.")
    return df

def compute_z_scores(df, output_dir, variable):
    selected_data = df[months].to_numpy()
    clean_values = selected_data[~np.isnan(selected_data)]
    mean = clean_values.mean()
    std = clean_values.std()
    print('mean\n', mean)
    print('std\n', std)

    z_scores = np.abs((df - mean)) / std
    z_scores['Year'] = df['Year']

     # Save the pivoted DataFrame to an Excel file
    output_file = os.path.join(output_dir, variable+'_Z_scores.xlsx')
    z_scores.to_excel(output_file, index=False)
    print(f"Z scores data saved to: {output_file}")
    print('z_scores\n', z_scores.head())
    return z_scores

def nullify_high_z_scores(df, output_dir, variable):
    z_scores = compute_z_scores(df, output_dir, variable)  # Assuming this returns same-shaped DataFrame
    
    # Create a mask of values to nullify
    to_nullify = z_scores > z_score_threshold
    
    # Make a copy to avoid SettingWithCopyWarning
    df_cleaned = df.copy()
    
    # Nullify values where Z-score exceeds threshold
    df_cleaned[to_nullify] = np.nan
    df_cleaned['Year'] = df['Year']  # Keep the Year column intact
    
    # Count affected values (not rows)
    num_nullified = to_nullify.sum().sum()
    print(f"Nullified {num_nullified} values with Z-scores above {z_score_threshold}")
    
    # Save the cleaned DataFrame to an Excel file
    print(f"Saving cleaned data to {output_dir} for variable {variable}")
    output_file = os.path.join(output_dir, variable+'_cleaned.xlsx')
    df_cleaned.to_excel(output_file, index=False)
    return df_cleaned





# Function calling
""" df, info = read_xks_excel(r"C:\Code\TIP\Balance_hidrico\input\estaciones_ideam\1_El Paraiso.xlsx")
output_dir = manage_station_directory(info['B2'])
variable = info['B6']
formatted_df = pivot_monthly_dataframe(df, output_dir, variable)
print(formatted_df.head())
clean_data_df = clean_data(formatted_df)
print(clean_data_df.head()) """

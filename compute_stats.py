import numpy as np
import os
import pandas as pd


from config import *
from read_xks import *
from format_data import pivot_monthly_dataframe
from clean_data import clean_data
from utils import manage_station_directory
from plot_histogram import plot_multiyear_monthly_histogram


def compute_stats(df):
    """
    Compute basic statistics for the DataFrame.
    Returns a dictionary with mean, std, min, max for each month.
    """
    #print(df.head(10))
    stats = {}
    for month in months:
        stats[month] = {
            'mean': df[month].mean(),
            'std': df[month].std(),
            'min': df[month].min(),
            'max': df[month].max(),
            'count': df[month].count(),
            'median': df[month].median(),
            'mode': df[month].mode()[0] if not df[month].mode().empty else np.nan,
            'Kurtosis': df[month].kurtosis(),
            'Skewness': df[month].skew()
        }
    return stats


def export_stats_to_excel(df, output_dir, variable):

    stats = compute_stats(df)
    # Convert stats dictionary to DataFrame
    stats_df = pd.DataFrame(stats)
    stats_df.reset_index(inplace=True)
    stats_df.rename(columns={'index': 'Stat'}, inplace=True)

    # Save the DataFrame to an Excel file
    output_file = os.path.join(output_dir, f"{variable}_stats.xlsx")
    stats_df.to_excel(output_file, index=False)
    print(f"Statistics saved to: {output_file}")
    return output_file





# Function calling
""" df, info = read_xks_excel(r"C:\Code\TIP\Balance_hidrico\input\estaciones_ideam\1_El Paraiso.xlsx")
output_dir = manage_station_directory(info['B2'])
variable = info['B6']
formatted_df = pivot_monthly_dataframe(df, output_dir, variable)
#print(formatted_df.head())
clean_data_df = clean_data(formatted_df)
print('#################')
print(clean_data_df.head(10))
export_stats_to_excel(clean_data_df, output_dir, variable)
plot_multiyear_monthly_histogram(
    clean_data_df, 
    f"Histograma Mensual Multianual - {variable}",
    variable_labels[variable],
    os.path.join(output_dir, f"{variable}_histograma.png")
    )
     """
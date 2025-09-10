import os
from config import *

from read_xks import *
from format_data import pivot_monthly_dataframe
from clean_data import clean_data
from utils import manage_station_directory
from plot_histogram import plot_multiyear_monthly_histogram
from compute_stats import export_stats_to_excel



#run the code for each file in a folder
current_file_parent_dir = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))
print('Current file parent dir: ', current_file_parent_dir)
input_dir = os.path.join(current_file_parent_dir, input_stations)
print('Input dir: ', input_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.xlsx') or filename.endswith('.xls'):
        file_path = os.path.join(input_dir, filename)

        print('Running script for file: ',file_path)
        
        df, info = read_xks_excel(file_path)
        output_dir = manage_station_directory(info['B2'])
        variable = info['B6']
        formatted_df = pivot_monthly_dataframe(df, output_dir, variable)
        #print(formatted_df.head())
        clean_data_df = clean_data(formatted_df, output_dir, variable)
        print('#################')
        print(clean_data_df.head(10))
        export_stats_to_excel(clean_data_df, output_dir, variable)
        plot_multiyear_monthly_histogram(
            clean_data_df, 
            f"Histograma Mensual Multianual - {variable}",
            variable_labels[variable],
            os.path.join(output_dir, f"{variable}_histograma.png")
            )
            
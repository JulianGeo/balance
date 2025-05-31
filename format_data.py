import pandas as pd
from read_xks import *
import os
from utils import manage_station_directory


def pivot_monthly_dataframe(df, output_dir, variable):

    df = df.copy()
    # First ensure the first column is datetime
    date_col = pd.to_datetime(df.iloc[:, 0], errors='coerce')
    if date_col.isna().any():
        print("Warning: Some dates couldn't be parsed. First few problematic values:")
        print(df.iloc[:, 0][date_col.isna()].head())
    
    df['Year'] = date_col.dt.year
    df['Month'] = date_col.dt.strftime('%b')
    
    # Group by Year and Month, aggregate by sum
    grouped = df.groupby(['Year', 'Month'])[df.columns[1]].sum().reset_index()
    
    pivot_df = grouped.pivot(index='Year', columns='Month', values=df.columns[1])
    
    # Ensure columns are ordered Jan-Dec
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    pivot_df = pivot_df.reindex(columns=[m for m in months_order if m in pivot_df.columns])
    
    pivot_df.reset_index(inplace=True)

    # Save the pivoted DataFrame to an Excel file
    output_file = os.path.join(output_dir, variable+'_raw.xlsx')
    pivot_df.to_excel(output_file, index=False)
    print(f"Raw formatted data saved to: {output_file}")
    return pivot_df

""" df, info = read_xks_excel(r"C:\Code\TIP\Balance_hidrico\input\estaciones_ideam\1_El Paraiso.xlsx")
output_dir = manage_station_directory(info['B2'])
variable = info['B6']
print(pivot_monthly_dataframe(df, output_dir, variable)) """
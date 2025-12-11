from dataframe_creator import read_excel_to_dataframe
from plots_creator import create_histograms
from config import *

df = read_excel_to_dataframe(excel_file_path, data_sheet_name)
df = df[df[complejo_volcanico_column_name] == complejo_volcanico_name]
df = df[df["Subcuenca"] == "Guaitara"]

print(len(df))

create_histograms(
    df,
    [
        "pH in situ",
        "T°",
        "Cl",
        "SO4",
        "HCO3",
        "Ca",
        "Mg",
        "Na",
        "K",
        "Li",
        "B",
        "SiO2",
    ],
)

from utils.dataframe_creator import read_excel_to_dataframe
from plots_creator import *
from .config import *
from clustering_analysis import *
from ionic_balance import calculate_ionic_balance
from . import stats

# This should be run from outside of this folder, like python -m preprocess.main
df = read_excel_to_dataframe(excel_file_path, data_sheet_name)
df = df[df[complejo_volcanico_column_name] == complejo_volcanico_name]
# df_guaitara = df[df["Subcuenca"] == "Guaitara"]

# Clean nan important columns

df = calculate_ionic_balance(df, iones)

stats.create_stats_table(
    df,
    sample_name_column="Nombre",
    parameters=[
        "pH in situ",
        "T°",
        "Cl",
        "SO4",
        "HCO3",
        "Ca",
        "Mg",
        "Na",
        "K",
    ],
    output_path=output_preprocess_path + r"\stats_table.xlsx",
)

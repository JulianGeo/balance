from dataframe_creator import read_excel_to_dataframe
from plots_creator import *
from config import *
from cluster_creator import *
from pca_analysis import *
from clustering_analysis import *
from ionic_balance import calculate_ionic_balance
from preprocess_data import log_transform_data

df = read_excel_to_dataframe(excel_file_path, data_sheet_name)
df = df[df[complejo_volcanico_column_name] == complejo_volcanico_name]
df_guaitara = df[df["Subcuenca"] == "Guaitara"]
df_mira = df[df["Subcuenca"] == "Mira"]
df_crater = df[df["Subcuenca"] == "Crater"]
df_no_crater = df[df["Subcuenca"] != "Crater"]


columns = [
    "pH in situ",
    "T°",
    "Cl",
    "SO4",
    "HCO3",
    "Ca",
    "Mg",
    "Na",
    "K",
    # "SiO2",
    # "Li",
    # "B",
]

log_transform_columns = ["Cl", "SO4", "HCO3", "Ca", "Mg", "Na", "K", "Li", "B"]


print(len(df))


"""

run_pca_analysis(
    df,
    columns,
    output_plots_path,
)
"""
# kMeans, X_scaled, labels = perform_clustering(df, n_clusters=3)
# plot_clustering_results(X_scaled, labels, output_dir=output_plots_path)

create_crossplot(df, "Cl", "SO4", "Nombre2")
df = calculate_ionic_balance(df_guaitara, iones)


df_log = log_transform_data(df, log_transform_columns)
# create_histograms([df_log], columns)


df_log = df[df["ionic_balance"].abs() <= 20]
# gemini_PCA(df_log, columns)

from dataframe_creator import read_excel_to_dataframe
from plots_creator import create_histograms
from config import *
from cluster_creator import *
from pca_analysis import *
from clustering_analysis import *

df = read_excel_to_dataframe(excel_file_path, data_sheet_name)
df = df[df[complejo_volcanico_column_name] == complejo_volcanico_name]
df_guaitara = df[df["Subcuenca"] == "Guaitara"]
df_mira = df[df["Subcuenca"] == "Mira"]
df_crater = df[df["Subcuenca"] == "Crater"]
dfs = [df_guaitara, df_mira]


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
    "Li",
    "B",
    "SiO2",
]

print(len(df))

"""

create_histograms(
    dfs,
    columns,
)
"""

"""

run_pca_analysis(
    df,
    columns,
    output_plots_path,
)
"""
# kMeans, X_scaled, labels = perform_clustering(df, n_clusters=3)
# plot_clustering_results(X_scaled, labels, output_dir=output_plots_path)

gemini_PCA(df, columns)

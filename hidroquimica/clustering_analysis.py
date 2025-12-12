import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.metrics import silhouette_score


# Ejecución de PCA
# Inicializamos PCA con todas las variables para ver la varianza
def run_pca(df, columns):

    # Drop rows with NA in the selected columns and return the filtered df
    df_clean = df.dropna(subset=columns)

    # Estandarizar los datos
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df_clean[columns])

    # Ejecutar PCA
    pca = PCA()
    pca.fit(scaled_data)

    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)

    return pca, scaled_data, cumulative_variance, df_clean


def plot_pca_results(cumulative_variance):

    plt.figure(figsize=(8, 5))
    plt.plot(
        range(1, len(cumulative_variance) + 1),
        cumulative_variance,
        marker="o",
        linestyle="--",
    )
    plt.title("Varianza Acumulada Explicada (Scree Plot)")
    plt.xlabel("Número de Componentes Principales")
    plt.ylabel("Varianza Acumulada (%)")
    plt.grid(True)
    # Sugerencia: Busque el punto donde la curva se "dobla" (el codo) o donde alcanza ~85-90%
    plt.axhline(y=0.85, color="r", linestyle="-")
    plt.text(1, 0.86, "85% Varianza", color="red")
    plt.show()

    """

    
    # Transformar los datos
    X_pca = pca.transform(scaled_data)
    pca_df = pd.DataFrame(X_pca, columns=[f'PC{i+1}' for i in range(X_pca.shape[1])])

    # Visualizar los primeros dos componentes principales
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='PC1', y='PC2', data=pca_df)
    plt.title('PCA - Primeras dos Componentes Principales')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.grid()
    plt.show()

    return pca_df"""


def k_optimization(cumulative_variance, X_scaled, index=None):
    # Determinar k: Tomamos el número de componentes que explican, por ejemplo, el 85%
    k = np.argmax(cumulative_variance >= 0.85) + 1
    print(
        f"\nSe seleccionan {k} Componentes Principales (PC) para explicar el 85% de la varianza."
    )

    # 2.4 Re-ejecutar PCA con el k óptimo
    pca_final = PCA(n_components=k)
    X_pca = pca_final.fit_transform(X_scaled)
    X_pca_df = pd.DataFrame(X_pca, columns=[f"PC{i+1}" for i in range(k)])
    # if an index (from the filtered df) is provided, assign it so labels match
    if index is not None:
        X_pca_df.index = index
    print(X_pca_df.head())
    return pca_final, k, X_pca, X_pca_df


def loading_analysis(pca_final, columns, k):
    loadings_df = pd.DataFrame(
        pca_final.components_.T,
        columns=[f"PC{i+1}" for i in range(k)],
        index=columns,
    )
    print("\n--- Cargas (Loadings) de PCA ---")
    print(
        "Interprete cada PC: valores altos (positivos/negativos) indican el proceso dominante."
    )
    print(loadings_df.round(3))

    # Visualización de las cargas
    plt.figure(figsize=(10, 6))
    sns.heatmap(
        loadings_df, annot=True, cmap="vlag", fmt=".2f", linewidths=0.5, center=0
    )
    plt.title("Heatmap de Cargas de PCA")
    plt.show()


def hierarchical_clustering(X_pca, df, X_pca_df, max_clusters=10):
    linked = linkage(X_pca, method="ward")

    plt.figure(figsize=(12, 6))
    dendrogram(
        linked,
        orientation="top",
        # labels=df.index.tolist(),
        labels=df.Termal.tolist(),
        distance_sort="descending",
        show_leaf_counts=True,
    )
    plt.title("Dendrograma de Clustering Jerárquico")
    plt.xlabel("Índice de Muestra")
    plt.ylabel("Distancia (Disimilitud de Ward)")
    # La altura donde "corta" el dendrograma define el número de clústeres
    plt.show()

    ### PAsar a otra función?
    # 4.3 Selección y Ejecución del Clustering
    # Basado en el dendrograma, seleccionamos un número de clústeres (ej. 4)
    # Debe ajustar este número (n_clusters=4) a lo que observe en el dendrograma.
    n_clusters_optimo = 4

    agg_clustering = AgglomerativeClustering(
        n_clusters=n_clusters_optimo, linkage="ward"
    )
    cluster_labels = agg_clustering.fit_predict(X_pca)

    df["Cluster_ID"] = cluster_labels
    X_pca_df["Cluster_ID"] = cluster_labels

    print(f"\n--- Conteo de Muestras por Clúster (k={n_clusters_optimo}) ---")
    print(df["Cluster_ID"].value_counts().sort_index())

    return n_clusters_optimo


def zoning_validation(df, X_pca_df, pca_final, n_clusters_optimo):
    # 5.1 Validación con la variable SubCuenca
    print("\n--- Validación Cruzada: Subcuenca vs. Cluster_ID ---")
    print(pd.crosstab(df["Subcuenca"], df["Cluster_ID"]))

    # 5.2 Visualización Final de Clústeres en el Espacio PCA
    plt.figure(figsize=(10, 8))
    sns.scatterplot(
        x=X_pca_df["PC1"],
        y=X_pca_df["PC2"],
        hue="Cluster_ID",
        style=df["Subcuenca"],
        palette="viridis",
        s=150,
        data=X_pca_df,
    )
    plt.title(f"Clústeres Identificados (k={n_clusters_optimo}) en Espacio PCA")
    plt.xlabel(f"PC1 ({pca_final.explained_variance_ratio_[0]*100:.1f} %)")
    plt.ylabel(f"PC2 ({pca_final.explained_variance_ratio_[1]*100:.1f} %)")
    plt.grid(True)
    plt.legend(title="Cluster ID / Subcuenca")
    plt.show()


def gemini_PCA(df, columns):
    pca, scaled_data, cummulative_variance, df_clean = run_pca(df, columns)
    plot_pca_results(cummulative_variance)
    pca_final, k, X_pca, X_pca_df = k_optimization(
        cummulative_variance, scaled_data, index=df_clean.index
    )
    loading_analysis(pca_final, columns, k)
    n_clusters_optimo = hierarchical_clustering(X_pca, df_clean, X_pca_df)
    zoning_validation(df_clean, X_pca_df, pca_final, n_clusters_optimo)

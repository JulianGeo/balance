import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt


def perform_clustering(df, n_clusters=3, random_state=42):
    """
    Perform K-means clustering on numerical columns of a dataframe.

    Args:
        df (pd.DataFrame): Input dataframe
        n_clusters (int): Number of clusters
        random_state (int): Random state for reproducibility

    Returns:
        tuple: (fitted KMeans model, scaled data, cluster labels)
    """
    # Select only numerical columns
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    X = df[numerical_cols].dropna()

    # Standardize the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    return kmeans, X_scaled, labels, X.index


def plot_clustering_results(X_scaled, labels, output_dir="./"):
    """
    Plot clustering results and save figures.

    Args:
        X_scaled (np.ndarray): Scaled feature matrix
        labels (np.ndarray): Cluster labels
        output_dir (str): Directory to save plots
    """
    # PCA for visualization
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # Plot 1: PCA scatter plot
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap="viridis", s=100)
    plt.xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)")
    plt.ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)")
    plt.title("Clustering Results - PCA")
    plt.colorbar(scatter, label="Cluster")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/clustering_pca.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Plot 2: Cluster distribution
    plt.figure(figsize=(8, 5))
    unique, counts = np.unique(labels, return_counts=True)
    plt.bar(unique, counts, color="skyblue", edgecolor="black")
    plt.xlabel("Cluster")
    plt.ylabel("Number of Samples")
    plt.title("Cluster Distribution")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/cluster_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Plots saved to {output_dir}")

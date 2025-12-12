import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def perform_pca(data, columns):

    data = data.dropna(subset=columns)
    # Standardize the data
    scaled_data = StandardScaler().fit_transform(data[columns])

    # Perform PCA
    pca = PCA()
    principal_components = pca.fit_transform(scaled_data)

    # Create a DataFrame with the principal components
    pca_df = pd.DataFrame(
        data=principal_components, columns=[f"PC{i+1}" for i in range(len(columns))]
    )
    return pca_df, pca


def plot_pca(pca_df, pca, output_file):
    plt.figure(figsize=(10, 7))
    plt.scatter(pca_df["PC1"], pca_df["PC2"], alpha=0.5)
    plt.title("PCA Result")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid()
    plt.savefig(output_file)
    plt.show()
    plt.close()


def run_pca_analysis(data, columns, output_file):
    pca_df, pca = perform_pca(data, columns)
    plot_pca(pca_df, pca, output_file)


# Example usage:
# data = pd.read_csv('your_data.csv')
# run_pca_analysis(data, ['column1', 'column2', 'column3'], 'pca_plot.png')

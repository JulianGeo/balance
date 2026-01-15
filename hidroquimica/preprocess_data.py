import numpy as np
import pandas as pd


def log_transform_data(df_pca, log_transform_columns):
    """Apply log transformation to specified columns."""

    df_pca[log_transform_columns] = df_pca[log_transform_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    print("pre", df_pca[log_transform_columns].head())

    epsilon = 1e-12
    for col in log_transform_columns:
        # Handle NaN/null values - keep them as NaN
        mask = df_pca[col].notna()
        df_pca.loc[mask, col] = np.log(df_pca.loc[mask, col] + epsilon)

    print("post", df_pca[log_transform_columns].head())
    return df_pca

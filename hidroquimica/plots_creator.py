import pandas as pd
from pathlib import Path
from config import *

import matplotlib.pyplot as plt


def create_histograms(dataframes, column_names, output_dir=output_plots_path):
    """
    Create and save overlapped histograms for each column across multiple dataframes.

    Args:
        dataframes: list of pandas DataFrames or a single DataFrame
        column_names: list of column names to create histograms for
        output_dir: directory to save histogram images
    """
    # Handle single dataframe
    if isinstance(dataframes, pd.DataFrame):
        dataframes = [dataframes]

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    colors = plt.cm.tab10(range(len(dataframes)))

    for column in column_names:
        plt.figure(figsize=(10, 6))

        for idx, df in enumerate(dataframes):
            if column in df.columns:
                numeric_data = pd.to_numeric(df[column], errors="coerce")
                numeric_data = numeric_data.dropna()

                if len(numeric_data) > 0:
                    numeric_data.hist(
                        bins=50,
                        alpha=0.6,
                        edgecolor="black",
                        color=colors[idx],
                        label=f"DataFrame {df['Subcuenca'].iloc[0]}",
                    )
                else:
                    print(f'DataFrame {idx}: Column "{column}" has no numeric data')
            else:
                print(f'DataFrame {idx}: Column "{column}" not found')

        plt.title(f"Histogram of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.legend()
        plt.grid(axis="y", alpha=0.3)

        filename = output_path / f"{column}_histogram.png"
        plt.savefig(filename, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Saved: {filename}")

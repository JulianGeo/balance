import pandas as pd
from pathlib import Path
from config import *

import matplotlib.pyplot as plt


def create_histograms(dataframe, column_names, output_dir=output_plots_path):
    """
    Create and save histograms for each column in the dataframe.

    Args:
        dataframe: pandas DataFrame containing the data
        column_names: list of column names to create histograms for
        output_dir: directory to save histogram images
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for column in column_names:
        if column in dataframe.columns:
            # Convert to numeric, coercing errors to NaN
            numeric_data = pd.to_numeric(dataframe[column], errors="coerce")
            # Filter out NaN values
            numeric_data = numeric_data.dropna()

            if len(numeric_data) > 0:
                plt.figure(figsize=(10, 6))
                numeric_data.hist(bins=30, edgecolor="black")
                plt.title(f"Histogram of {column}")
                plt.xlabel(column)
                plt.ylabel("Frequency")
                plt.grid(axis="y", alpha=0.3)

                filename = output_path / f"{column}_histogram.png"
                plt.savefig(filename, dpi=300, bbox_inches="tight")
                plt.close()
                print(f"Saved: {filename}")
            else:
                print(f'Column "{column}" has no numeric data')
        else:
            print(f'Column "{column}" not found in dataframe')

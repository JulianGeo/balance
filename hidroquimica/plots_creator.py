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


def create_crossplot(
    dataframe, x_column, y_column, tag_column, output_dir=output_plots_path
):
    """
    Create and save a crossplot for two columns with points tagged by a third column.

    Args:
        dataframe: pandas DataFrame
        x_column: name of column for x-axis
        y_column: name of column for y-axis
        tag_column: name of column to tag/color each point
        output_dir: directory to save crossplot image
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Convert to numeric and drop NaN
    x_data = pd.to_numeric(dataframe[x_column], errors="coerce")
    y_data = pd.to_numeric(dataframe[y_column], errors="coerce")
    tags = dataframe[tag_column]

    # Create mask for valid data
    mask = x_data.notna() & y_data.notna()
    x_data = x_data[mask]
    y_data = y_data[mask]
    tags = tags[mask]

    plt.figure(figsize=(10, 6))

    # Plot each tag group with different colors and markers
    colors = plt.cm.tab10(range(len(tags.unique())))
    markers = ["o", "s", "^", "D", "v", "*", "p", "H", "+", "x"]

    for idx, tag in enumerate(tags.unique()):
        tag_mask = tags == tag
        plt.scatter(
            x_data[tag_mask],
            y_data[tag_mask],
            color=colors[idx % len(colors)],
            marker=markers[idx % len(markers)],
            alpha=0.6,
            edgecolor="black",
            s=50,
            label=tag,
        )

    plt.ylim(0.1, 10000)
    plt.xscale("linear")
    plt.yscale("log")
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    # plt.title(f"Crossplot: {x_column} vs {y_column}")
    plt.legend(title="Spring", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.grid(alpha=0.3)

    filename = output_path / f"{x_column}_vs_{y_column}_crossplot.svg"
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


def group_by_element(df: pd.DataFrame) -> dict:
    """
    Groups the dataframe by the 'element' column.

    Returns:
        dict: A dictionary where keys are unique elements and values are grouped DataFrames.
    """

    grouped = {element: group for element, group in df.groupby("elemento")}
    return grouped


def plot_histograms_with_error(groups: dict):
    """
    Plots histograms for each group with two series: 'fraccion_reservorio' and 'fraccion_meteorica'.
    Error bars are plotted on the bars.

    Args:
        groups (dict): Dictionary of grouped DataFrames by 'element'.
    """
    for element, group in groups.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        bins = np.linspace(0, 1, 11)

        # Calculate means and stds for error bars
        res_data = group["fraccion_reservorio"].dropna()
        met_data = group["fraccion_meteorica"].dropna()

        res_hist, _ = np.histogram(res_data, bins=bins)
        met_hist, _ = np.histogram(met_data, bins=bins)

        res_err = np.sqrt(res_hist)
        met_err = np.sqrt(met_hist)

        width = 0.4
        ax.bar(
            bins[:-1] - width / 2,
            res_hist,
            width=width,
            label="Fraccion Reservorio",
            yerr=res_err,
            capsize=5,
            alpha=0.7,
        )
        ax.bar(
            bins[:-1] + width / 2,
            met_hist,
            width=width,
            label="Fraccion Meteorica",
            yerr=met_err,
            capsize=5,
            alpha=0.7,
        )

        ax.set_xlim(0, 1)
        ax.set_xlabel("Fraction")
        ax.set_ylabel("Count")
        ax.set_title(f"Histogram for element: {element}")
        ax.legend()
        plt.tight_layout()
        plt.show()


def plot_histograms_with_lines(groups: dict):
    """
    Plots histograms for each group with two series: 'fraccion_reservorio' and 'fraccion_meteorica'
    using continuous lines instead of bars.

    Args:
        groups (dict): Dictionary of grouped DataFrames by 'element'.
    """
    for element, group in groups.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        bins = np.linspace(0, 1, 101)

        res_data = group["fraccion_reservorio"].dropna()
        met_data = group["fraccion_meteorica"].dropna()

        res_hist, bin_edges = np.histogram(res_data, bins=bins, density=True)
        met_hist, _ = np.histogram(met_data, bins=bins, density=True)

        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        ax.plot(
            bin_centers,
            res_hist,
            label="Fraccion Reservorio",
            color="blue",
            linewidth=2,
        )
        ax.plot(
            bin_centers,
            met_hist,
            label="Fraccion Meteorica",
            color="orange",
            linewidth=2,
        )

        ax.set_xlim(0, 1)
        ax.set_xlabel("Fraction")
        ax.set_ylabel("Density")
        ax.set_title(f"Histogram (lines) for element: {element}")
        ax.legend()
        plt.tight_layout()
        plt.show()


def plot_traditional_histograms(groups: dict):
    """
    Plots traditional histograms (bar style) for each group with two series: 'fraccion_reservorio' and 'fraccion_meteorica'.

    Args:
        groups (dict): Dictionary of grouped DataFrames by 'element'.
    """
    for element, group in groups.items():
        fig, ax = plt.subplots(figsize=(8, 5))
        bins = np.linspace(0, 1, 21)

        res_data = group["fraccion_reservorio"].dropna()
        met_data = group["fraccion_meteorica"].dropna()

        ax.hist(
            res_data,
            bins=bins,
            alpha=0.6,
            label="Fraccion Reservorio",
            color="blue",
            edgecolor="black",
        )
        ax.hist(
            met_data,
            bins=bins,
            alpha=0.6,
            label="Fraccion Meteorica",
            color="orange",
            edgecolor="black",
        )

        ax.set_xlim(0, 1)
        ax.set_xlabel("Fracción")
        ax.set_ylabel("Conteo")
        ax.set_title(f"Histograma para el elemento: {element}")
        ax.legend()
        plt.tight_layout()
        plt.show()


def generate_plot(df: pd.DataFrame):
    """
    Generates histograms with error bars for each element in the DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame containing 'element', 'fraccion_reservorio', and 'fraccion_meteorica' columns.
    """
    grouped = group_by_element(df)
    # plot_histograms_with_error(grouped)
    plot_traditional_histograms(grouped)
    # plot_histograms_with_lines(grouped)

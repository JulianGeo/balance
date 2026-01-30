import pandas as pd
from config import *
import numpy as np
import matplotlib.pyplot as plt


def read_excel_to_dataframe(file_path, sheet_name=0):
    """
    Reads an Excel file and returns a pandas DataFrame.

    Parameters:
        file_path (str): Path to the Excel file.
        sheet_name (str or int, optional): Name or index of the sheet to read. Defaults to first sheet.

    Returns:
        pd.DataFrame: DataFrame containing the Excel data.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df = df[[col for col in df.columns if col in spyder_variables.values()]]
    print(df.head())
    return df


def plot_spyder(df, spyder_variables, title="Spyder Plot"):
    """
    Generates a spyder (radar) plot for the specified variables.
    Each row in the DataFrame is plotted as a separate series.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        spyder_variables (dict): Dictionary where keys are display names and values are column names in df.
        title (str): Title of the plot.
    """
    labels = list(spyder_variables.keys())
    columns = list(spyder_variables.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(subplot_kw={"polar": True})

    for idx, row in df[columns].iterrows():
        values = row.values
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, "o-", linewidth=1, label=str(idx))
        ax.fill(angles, values, alpha=0.1)

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_title(title)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    plt.show()


def plot_spyder2(df, spyder_variables, axis_ranges, title="Star Plot"):
    """
    Generates a star plot (radar plot) where each axis represents a different variable,
    and each axis is scaled independently according to axis_ranges.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        spyder_variables (dict): Dictionary where keys are display names and values are column names in df.
        axis_ranges (dict): Dictionary where keys are column names and values are (min, max) tuples for axis scaling.
        title (str): Title of the plot.
    """
    labels = list(spyder_variables.keys())
    columns = list(spyder_variables.values())
    num_vars = len(labels)

    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)
    angles = np.concatenate((angles, [angles[0]]))

    fig, ax = plt.subplots(subplot_kw={"polar": True})

    # Normalize each value according to its axis range
    for idx, row in df[columns].iterrows():
        values = []
        for col in columns:
            min_val, max_val = axis_ranges[col]
            val = row[col]
            # Avoid division by zero
            if max_val - min_val == 0:
                norm_val = 0
            else:
                norm_val = (val - min_val) / (max_val - min_val)
            values.append(norm_val)
        values = np.array(values)
        values = np.concatenate((values, [values[0]]))
        ax.plot(angles, values, "o-", linewidth=1, label=str(idx))
        # Removed ax.fill to eliminate shadows

    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_title(title)
    ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
    plt.show()


def generate_random_spyder_data(spyder_variables, num_series=3, seed=None):
    """
    Generates a DataFrame with random values for spyder plot.

    Parameters:
        spyder_variables (dict): Dictionary where keys are display names and values are column names.
        num_series (int): Number of series (rows) to generate.
        seed (int, optional): Random seed for reproducibility.

    Returns:
        pd.DataFrame: DataFrame with random values.
    """
    if seed is not None:
        np.random.seed(seed)
    columns = list(spyder_variables.values())
    data = np.random.rand(num_series, len(columns))
    df = pd.DataFrame(data, columns=columns)
    print(df.head())
    return df


#### stackoverflow sample
def spider(df, *, id_column, title=None, max_values=None, padding=1.25):
    categories = df._get_numeric_data().columns.tolist()
    data = df[categories].to_dict(orient="list")
    ids = df[id_column].tolist()
    if max_values is None:
        max_values = {key: padding * max(value) for key, value in data.items()}

    normalized_data = {
        key: np.array(value) / max_values[key] for key, value in data.items()
    }
    num_vars = len(data.keys())
    tiks = list(data.keys())
    tiks += tiks[:1]
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist() + [0]
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i, model_name in enumerate(ids):
        values = [normalized_data[key][i] for key in data.keys()]
        actual_values = [data[key][i] for key in data.keys()]
        values += values[:1]  # Close the plot for a better look
        ax.plot(angles, values, label=model_name)
        # ax.fill(angles, values, alpha=0.15)
        for _x, _y, t in zip(angles, values, actual_values):
            t = f"{t:.2f}" if isinstance(t, float) else str(t)
            # ax.text(_x, _y, t, size="xx-small")

    # ax.fill(angles, np.ones(num_vars + 1), alpha=0.05)
    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(tiks)
    ax.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))
    if title is not None:
        plt.suptitle(title)
    plt.show()


df = read_excel_to_dataframe(excel_file_path)
radar = spider

"""
spider(
    pd.DataFrame(
        {
            "x": [*"abcde"],
            "c1": [10, 11, 12, 13, 14],
            "c2": [0.1, 0.3, 0.4, 0.1, 0.9],
            "c3": [1e5, 2e5, 3.5e5, 8e4, 5e4],
            "c4": [9, 12, 5, 2, 0.2],
            "test": [1, 1, 1, 1, 5],
        }
    ),
    id_column="x",
    title="Sample Spider",
    padding=1.1,
)
"""
spider(
    df,
    id_column=spyder_variables["ID"],
    title="Sample Spider",
    padding=1.1,
)


# Example usage:
# random_df = generate_random_spyder_data(spyder_variables, num_series=3, seed=42)
# plot_spyder(random_df, spyder_variables, title="Random Spyder Plot")


df = read_excel_to_dataframe(excel_file_path)

"""
axis_ranges = {
    "PH": (0, 120),
    "Coliformes Totales (NMP/100 mL)": (0, 120),
    "ARSENICO": (0, 120),
    "NITRATOS": (0, 120),
    "Plomo": (0, 120),
    "CADMIO": (0, 120),
    "SULFATOS": (0, 120),
}
plot_spyder2(df, spyder_variables, axis_ranges, title="Spyder Plot Example")

"""

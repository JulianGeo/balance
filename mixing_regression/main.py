import pandas as pd
from config import *
import itertools


def read_excel_file(file_path):
    """
    Reads an Excel file and returns a pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file.

    Returns:
        pd.DataFrame: DataFrame containing the Excel data.
    """
    return pd.read_excel(file_path)


def generate_grouped_subsets(df, group_col=keywords["name"]):
    """
    Groups the DataFrame by `group_col` and generates all possible subsets
    with one row per group.

    Args:
        df (pd.DataFrame): Input DataFrame.
        group_col (str): Column name to group by.

    Returns:
        List[pd.DataFrame]: List of DataFrames, each containing one row per group.
    """
    grouped = [group for _, group in df.groupby(group_col)]
    row_lists = [group.iterrows() for group in grouped]
    row_lists = [[row[1] for row in group.iterrows()] for group in grouped]
    all_combinations = itertools.product(*row_lists)
    output = [pd.DataFrame(list(rows)) for rows in all_combinations]
    return output


df = read_excel_file(chemical_file_path)
df_samples_sets = generate_grouped_subsets(df)
print(len(df_samples_sets))

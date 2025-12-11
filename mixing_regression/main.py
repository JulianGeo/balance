import pandas as pd
from config import *
from simple_mixing_regression import *
from stats import *
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


def generate_grouped_samples_sets(df, group_col=keyword["name"]):
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


def compute_mixing_results(df_samples_sets):
    samples_results = []
    for i, df_sample in enumerate(df_samples_sets):
        # print(f"\n--- Sample Set {i+1} ---")
        mixing_sample_results = run_mixing_model_with_adapter(df_sample)
        if mixing_sample_results is not None:
            # print(mixing_sample_results)
            samples_results.append(mixing_sample_results)

    combined_results = pd.concat(samples_results, ignore_index=True)
    print(combined_results.head())
    return combined_results


####USAGE EXAMPLE####
df = read_excel_file(chemical_file_path)
df_samples_sets = generate_grouped_samples_sets(df)
combined_results = compute_mixing_results(df_samples_sets)

generate_plot(combined_results)
combined_results.to_excel(
    r"C:\Code\TIP\Balance_hidrico\results\mixing_model\results.xlsx", index=False
)

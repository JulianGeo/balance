import pandas as pd


def read_excel_to_dataframe(file_path, sheet_name=0):
    """
    Read an Excel file and return as a pandas DataFrame.

    Args:
        file_path (str): Path to the Excel file
        sheet_name (int or str): Sheet name or index (default: 0)

    Returns:
        pd.DataFrame: DataFrame containing the Excel data
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df


# Example usage:
if __name__ == "__main__":
    # Read Excel file
    df = read_excel_to_dataframe("your_file.xlsx")

    # Display the dataframe
    print(df.head())

    # Optionally export to another format
    # df.to_csv("output.csv", index=False)

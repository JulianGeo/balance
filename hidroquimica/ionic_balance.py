from config import *
import pandas as pd


def calculate_meq(value, molecular_weight):
    """Convert ion concentration (mg/L) to milliequivalents (meq/L).

    Treat missing or non-numeric values as zero. Raise if molecular weight
    is missing or zero to avoid silent division errors.
    """
    if molecular_weight is None or molecular_weight == 0:
        raise ValueError("molecular_weight must be a non-zero number")

    # pandas.isna covers None and NaN
    if pd.isna(value):
        return 0

    try:
        val = float(value)
    except (TypeError, ValueError):
        return 0

    if val == 0:
        return 0

    return val / molecular_weight


def calculate_ionic_balance(df, iones):
    """
    Calculate ionic balance for water samples.

    Parameters:
    df: DataFrame with ion concentrations (mg/L)
    iones: dict with ion names as keys and molecular weights as values

    Returns:
    DataFrame with meq/L values and ionic balance percentage
    """
    meq_df = df.copy()

    # Calculate meq/L for each ion
    for ion, mw in iones.items():
        if ion in df.columns:
            meq_df[f"{ion}_meq"] = df[ion].apply(lambda x: calculate_meq(x, mw))
        else:
            meq_df[f"{ion}_meq"] = 0

    # Separate cations and anions
    cations = ["Na", "Ca", "Mg", "K"]
    anions = ["HCO3", "CO3", "Cl", "SO4"]

    # Sum meq/L
    meq_df["sum_cations"] = meq_df[
        [f"{ion}_meq" for ion in cations if f"{ion}_meq" in meq_df.columns]
    ].sum(axis=1)
    meq_df["sum_anions"] = meq_df[
        [f"{ion}_meq" for ion in anions if f"{ion}_meq" in meq_df.columns]
    ].sum(axis=1)

    # Calculate ionic balance percentage
    meq_df["ionic_balance"] = (
        (meq_df["sum_cations"] - meq_df["sum_anions"])
        / (meq_df["sum_cations"] + meq_df["sum_anions"])
        * 100
    )

    print(meq_df.head())

    return meq_df

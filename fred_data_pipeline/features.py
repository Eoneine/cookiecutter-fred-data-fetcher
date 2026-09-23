import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the combined long-format DataFrame from the FRED API.
    Converts dates to datetime, handles missing values denoted by '.', 
    and removes duplicates.

    Args:
        df (pd.DataFrame): Raw combined DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(
        df["value"].replace(".", pd.NA), errors="coerce"
    )
    df = df.drop_duplicates(subset=["series_id", "date"])
    return df

def reshape_data(df_long: pd.DataFrame, output_format: str = "long") -> pd.DataFrame:
    """
    Reshape the clean DataFrame into either long or wide format.

    Args:
        df_long (pd.DataFrame): Cleaned data in long format.
        output_format (str): The desired output format, 'long' or 'wide'. Defaults to "long".

    Returns:
        pd.DataFrame: Reshaped DataFrame according to the requested format.

    Raises:
        ValueError: If an unknown output_format is provided.
    """
    if output_format == "long":
        return df_long.copy()
    elif output_format == "wide":
        df_wide = df_long.pivot(index="date", columns="series_id", values="value")
        return df_wide.reset_index()
    else:
        raise ValueError(f"Unknown output_format: '{output_format}'. Use 'long' or 'wide'.")

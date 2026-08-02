from pathlib import Path

import pandas as pd


NCR_CITIES = ["Delhi", "Ghaziabad", "Faridabad"]


def load_crime_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load the raw crime dataset from a CSV file.
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    return pd.read_csv(file_path)


def filter_ncr_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Keep only Delhi NCR cities available in the dataset.
    """
    return df[df["City"].isin(NCR_CITIES)].copy()


def clean_crime_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean missing values and convert date columns.
    """
    cleaned_df = df.copy()

    cleaned_df["Weapon Used"] = (
        cleaned_df["Weapon Used"]
        .fillna("Unknown")
    )

    cleaned_df["Date Reported"] = pd.to_datetime(
        cleaned_df["Date Reported"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    cleaned_df["Date of Occurrence"] = pd.to_datetime(
        cleaned_df["Date of Occurrence"],
        format="%m-%d-%Y %H:%M",
        errors="coerce"
    )

    cleaned_df["Time of Occurrence"] = pd.to_datetime(
        cleaned_df["Time of Occurrence"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    cleaned_df["Date Case Closed"] = pd.to_datetime(
        cleaned_df["Date Case Closed"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    return cleaned_df


def prepare_crime_data(file_path: str | Path) -> pd.DataFrame:
    """
    Run the complete loading, filtering, and cleaning pipeline.
    """
    df = load_crime_data(file_path)
    df = filter_ncr_data(df)
    df = clean_crime_data(df)

    return df
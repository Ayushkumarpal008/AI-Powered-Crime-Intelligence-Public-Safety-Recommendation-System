import pandas as pd


def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create date and time-based features.
    """
    featured_df = df.copy()

    featured_df["Year"] = featured_df["Date of Occurrence"].dt.year
    featured_df["Month"] = featured_df["Date of Occurrence"].dt.month
    featured_df["MonthName"] = (
        featured_df["Date of Occurrence"].dt.month_name()
    )
    featured_df["Day"] = featured_df["Date of Occurrence"].dt.day
    featured_df["DayOfWeek"] = (
        featured_df["Date of Occurrence"].dt.day_name()
    )
    featured_df["Hour"] = featured_df["Date of Occurrence"].dt.hour

    featured_df["IsWeekend"] = featured_df["DayOfWeek"].isin(
        ["Saturday", "Sunday"]
    )

    featured_df["IsNightCrime"] = (
        (featured_df["Hour"] >= 20)
        | (featured_df["Hour"] <= 5)
    )

    return featured_df


def create_victim_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create victim age-group features.
    """
    featured_df = df.copy()

    bins = [0, 18, 30, 45, 60, float("inf")]

    labels = [
        "Child",
        "Young Adult",
        "Adult",
        "Middle Age",
        "Senior"
    ]

    featured_df["VictimAgeGroup"] = pd.cut(
        featured_df["Victim Age"],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    return featured_df


def create_case_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create case-status and resolution-time features.
    """
    featured_df = df.copy()

    featured_df["IsCaseClosed"] = (
        featured_df["Case Closed"]
        .str.strip()
        .str.upper()
        .eq("YES")
    )

    featured_df["CaseResolutionDays"] = (
        featured_df["Date Case Closed"]
        - featured_df["Date Reported"]
    ).dt.days

    return featured_df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the complete feature-engineering pipeline.
    """
    df = create_time_features(df)
    df = create_victim_features(df)
    df = create_case_features(df)

    return df
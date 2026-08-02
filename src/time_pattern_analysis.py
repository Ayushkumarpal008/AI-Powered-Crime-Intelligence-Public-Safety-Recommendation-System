import pandas as pd


def get_peak_crime_hour(df: pd.DataFrame) -> dict:
    """
    Return the hour with the highest number of recorded crimes.
    """
    hourly_counts = df["Hour"].value_counts()

    peak_hour = int(hourly_counts.idxmax())
    peak_count = int(hourly_counts.max())

    return {
        "peak_hour": peak_hour,
        "crime_count": peak_count
    }


def get_peak_crime_day(df: pd.DataFrame) -> dict:
    """
    Return the weekday with the highest number of crimes.
    """
    day_counts = df["DayOfWeek"].value_counts()

    peak_day = day_counts.idxmax()
    peak_count = int(day_counts.max())

    return {
        "peak_day": peak_day,
        "crime_count": peak_count
    }


def get_peak_crime_month(df: pd.DataFrame) -> dict:
    """
    Return the month with the highest number of crimes.
    """
    month_counts = df["MonthName"].value_counts()

    peak_month = month_counts.idxmax()
    peak_count = int(month_counts.max())

    return {
        "peak_month": peak_month,
        "crime_count": peak_count
    }


def get_city_hour_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts by city and hour.
    """
    result = (
        df.groupby(["City", "Hour"])
        .size()
        .reset_index(name="CrimeCount")
        .sort_values(["City", "Hour"])
    )

    return result


def get_city_peak_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the peak crime hour for each city.
    """
    city_hour_counts = (
        df.groupby(["City", "Hour"])
        .size()
        .reset_index(name="CrimeCount")
    )

    peak_rows = city_hour_counts.loc[
        city_hour_counts.groupby("City")["CrimeCount"].idxmax()
    ]

    return peak_rows.reset_index(drop=True)


def get_crime_type_hour_pattern(
    df: pd.DataFrame,
    crime_type: str
) -> pd.DataFrame:
    """
    Return the hourly pattern for a selected crime type.
    """
    filtered_df = df[
        df["Crime Description"].str.upper() == crime_type.upper()
    ]

    result = (
        filtered_df["Hour"]
        .value_counts()
        .reindex(range(24), fill_value=0)
        .sort_index()
        .rename_axis("Hour")
        .reset_index(name="CrimeCount")
    )

    return result


def get_crime_type_peak_hours(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Return the peak hour for the most common crime types.
    """
    top_crimes = (
        df["Crime Description"]
        .value_counts()
        .head(top_n)
        .index
    )

    filtered_df = df[
        df["Crime Description"].isin(top_crimes)
    ]

    grouped = (
        filtered_df.groupby(["Crime Description", "Hour"])
        .size()
        .reset_index(name="CrimeCount")
    )

    peak_rows = grouped.loc[
        grouped.groupby("Crime Description")["CrimeCount"].idxmax()
    ]

    return (
        peak_rows
        .sort_values("CrimeCount", ascending=False)
        .reset_index(drop=True)
    )


def get_day_hour_heatmap_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return weekday-hour crime counts in pivot-table format.
    """
    weekday_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday"
    ]

    result = pd.pivot_table(
        df,
        index="DayOfWeek",
        columns="Hour",
        values="Report Number",
        aggfunc="count",
        fill_value=0
    )

    result = result.reindex(weekday_order)

    return result


def get_city_day_night_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return day and night crime counts for each city.
    """
    temp_df = df.copy()

    temp_df["TimePeriod"] = temp_df["IsNightCrime"].map({
        False: "Day",
        True: "Night"
    })

    result = (
        temp_df.groupby(["City", "TimePeriod"])
        .size()
        .reset_index(name="CrimeCount")
    )

    return result


def get_time_period(hour: int) -> str:
    """
    Convert an hour into a readable time period.
    """
    if 5 <= hour < 12:
        return "Morning"

    if 12 <= hour < 17:
        return "Afternoon"

    if 17 <= hour < 21:
        return "Evening"

    return "Night"


def add_time_period(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add Morning, Afternoon, Evening, or Night labels.
    """
    result = df.copy()

    result["TimePeriod"] = result["Hour"].apply(get_time_period)

    return result


def get_time_period_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts by broad time period.
    """
    temp_df = add_time_period(df)

    order = [
        "Morning",
        "Afternoon",
        "Evening",
        "Night"
    ]

    result = (
        temp_df["TimePeriod"]
        .value_counts()
        .reindex(order, fill_value=0)
        .rename_axis("TimePeriod")
        .reset_index(name="CrimeCount")
    )

    return result
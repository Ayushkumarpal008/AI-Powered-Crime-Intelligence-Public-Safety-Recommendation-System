import pandas as pd


def get_city_crime_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return the number of crime records for each city.
    """
    result = (
        df["City"]
        .value_counts()
        .rename_axis("City")
        .reset_index(name="CrimeCount")
    )

    return result


def get_top_crime_types(
    df: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    """
    Return the most frequently recorded crime types.
    """
    result = (
        df["Crime Description"]
        .value_counts()
        .head(top_n)
        .rename_axis("CrimeDescription")
        .reset_index(name="CrimeCount")
    )

    return result


def get_monthly_crime_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts grouped by year and month.
    """
    result = (
        df.groupby(["Year", "Month", "MonthName"])
        .size()
        .reset_index(name="CrimeCount")
        .sort_values(["Year", "Month"])
    )

    return result


def get_weekday_crime_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts for each day of the week.
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

    result = (
        df["DayOfWeek"]
        .value_counts()
        .reindex(weekday_order, fill_value=0)
        .rename_axis("DayOfWeek")
        .reset_index(name="CrimeCount")
    )

    return result


def get_hourly_crime_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts for each hour of the day.
    """
    result = (
        df["Hour"]
        .value_counts()
        .reindex(range(24), fill_value=0)
        .sort_index()
        .rename_axis("Hour")
        .reset_index(name="CrimeCount")
    )

    return result


def get_weekend_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare weekday and weekend crime counts.
    """
    result = (
        df["IsWeekend"]
        .map({
            False: "Weekday",
            True: "Weekend"
        })
        .value_counts()
        .rename_axis("DayType")
        .reset_index(name="CrimeCount")
    )

    return result


def get_day_night_comparison(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compare daytime and nighttime crime counts.
    """
    result = (
        df["IsNightCrime"]
        .map({
            False: "Day",
            True: "Night"
        })
        .value_counts()
        .rename_axis("TimePeriod")
        .reset_index(name="CrimeCount")
    )

    return result


def get_victim_age_group_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return crime counts for each victim age group.
    """
    result = (
        df["VictimAgeGroup"]
        .value_counts(sort=False)
        .rename_axis("VictimAgeGroup")
        .reset_index(name="CrimeCount")
    )

    return result


def get_case_status_counts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return open and closed case counts.
    """
    result = (
        df["IsCaseClosed"]
        .map({
            True: "Closed",
            False: "Open"
        })
        .value_counts()
        .rename_axis("CaseStatus")
        .reset_index(name="CaseCount")
    )

    return result


def get_city_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a summary of crime statistics for each city.
    """
    result = (
        df.groupby("City")
        .agg(
            TotalCrimes=("Report Number", "count"),
            UniqueCrimeTypes=("Crime Description", "nunique"),
            AverageVictimAge=("Victim Age", "mean"),
            AveragePoliceDeployed=("Police Deployed", "mean"),
            ClosedCases=("IsCaseClosed", "sum"),
            NightCrimes=("IsNightCrime", "sum")
        )
        .reset_index()
    )

    result["CaseClosureRate"] = (
        result["ClosedCases"] / result["TotalCrimes"] * 100
    ).round(2)

    result["NightCrimePercentage"] = (
        result["NightCrimes"] / result["TotalCrimes"] * 100
    ).round(2)

    result["AverageVictimAge"] = (
        result["AverageVictimAge"].round(2)
    )

    result["AveragePoliceDeployed"] = (
        result["AveragePoliceDeployed"].round(2)
    )

    return result
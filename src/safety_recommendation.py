import pandas as pd


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


def get_city_statistics(
    df: pd.DataFrame,
    city: str
) -> dict:
    """
    Calculate important crime statistics for a selected city.
    """
    city_df = df[
        df["City"].str.lower() == city.lower()
    ].copy()

    if city_df.empty:
        return {}

    peak_hour = int(
        city_df["Hour"]
        .value_counts()
        .idxmax()
    )

    peak_day = (
        city_df["DayOfWeek"]
        .value_counts()
        .idxmax()
    )

    common_crime = (
        city_df["Crime Description"]
        .value_counts()
        .idxmax()
    )

    night_crime_percentage = round(
        city_df["IsNightCrime"].mean() * 100,
        2
    )

    closure_rate = round(
        city_df["IsCaseClosed"].mean() * 100,
        2
    )

    return {
        "city": city,
        "total_crimes": int(len(city_df)),
        "peak_hour": peak_hour,
        "peak_time_period": get_time_period(peak_hour),
        "peak_day": peak_day,
        "most_common_crime": common_crime,
        "night_crime_percentage": night_crime_percentage,
        "case_closure_rate": closure_rate
    }


def get_general_safety_tips() -> list[str]:
    """
    Return general public-safety recommendations.
    """
    return [
        "Stay aware of your surroundings, especially in crowded places.",
        "Avoid isolated or poorly lit routes during late hours.",
        "Keep emergency contacts available on your phone.",
        "Do not display expensive devices or jewellery unnecessarily.",
        "Share your travel details with a trusted person when travelling late.",
        "Use verified public transport or trusted ride-booking services.",
        "Report suspicious activity to the appropriate authorities."
    ]


def get_time_based_recommendations(hour: int) -> list[str]:
    """
    Return recommendations based on the selected hour.
    """
    period = get_time_period(hour)

    if period == "Morning":
        return [
            "Use busy and well-known routes.",
            "Stay alert near public transport locations.",
            "Keep personal belongings secure in crowded areas."
        ]

    if period == "Afternoon":
        return [
            "Remain cautious in busy markets and commercial areas.",
            "Protect your phone, wallet, and other valuables.",
            "Avoid sharing personal information with strangers."
        ]

    if period == "Evening":
        return [
            "Prefer well-lit and populated roads.",
            "Plan your return journey before leaving.",
            "Avoid isolated shortcuts."
        ]

    return [
        "Avoid travelling alone through isolated areas.",
        "Use verified transport services.",
        "Share live location with a trusted contact.",
        "Keep emergency numbers easily accessible.",
        "Prefer roads with good lighting and public activity."
    ]


def get_crime_specific_recommendations(
    crime_type: str
) -> list[str]:
    """
    Return recommendations based on a crime category.
    """
    crime = crime_type.strip().upper()

    recommendations = {
        "THEFT": [
            "Keep valuables out of sight.",
            "Use secure bags and keep them closed.",
            "Stay cautious in crowded locations."
        ],
        "ROBBERY": [
            "Avoid displaying cash or expensive devices.",
            "Do not resist if confronted by an armed offender.",
            "Move toward a populated area and contact authorities."
        ],
        "ASSAULT": [
            "Avoid confrontations and leave escalating situations.",
            "Stay in well-populated locations.",
            "Contact emergency services when immediate danger exists."
        ],
        "FRAUD": [
            "Never share OTPs, passwords, or banking PINs.",
            "Verify identities before transferring money.",
            "Avoid opening suspicious links or attachments."
        ],
        "CYBER CRIME": [
            "Use strong and unique passwords.",
            "Enable two-factor authentication.",
            "Do not share sensitive information through unknown websites."
        ],
        "DRUG OFFENSE": [
            "Avoid suspicious gatherings and unknown substances.",
            "Report illegal activity through appropriate channels.",
            "Do not accept packages from unknown individuals."
        ],
        "FIREARM OFFENSE": [
            "Leave the area immediately if weapons are visible.",
            "Do not attempt to intervene.",
            "Contact emergency services from a safe location."
        ],
        "ILLEGAL POSSESSION": [
            "Avoid handling suspicious or unknown items.",
            "Do not confront individuals involved in illegal activity.",
            "Inform authorities from a safe location."
        ]
    }

    return recommendations.get(
        crime,
        [
            "Stay aware of your surroundings.",
            "Avoid isolated areas during low-activity hours.",
            "Contact authorities if you observe suspicious activity."
        ]
    )


def calculate_pattern_level(
    selected_count: int,
    average_count: float
) -> str:
    """
    Classify the selected pattern using relative historical frequency.

    This is not a crime-risk score. It only compares the selected
    historical crime count with the dataset average.
    """
    if average_count <= 0:
        return "No Data"

    ratio = selected_count / average_count

    if ratio >= 1.5:
        return "High Historical Frequency"

    if ratio >= 0.75:
        return "Moderate Historical Frequency"

    return "Low Historical Frequency"


def generate_safety_recommendation(
    df: pd.DataFrame,
    city: str,
    hour: int,
    crime_type: str | None = None
) -> dict:
    """
    Generate user-facing recommendations using historical patterns.
    """
    city_df = df[
        df["City"].str.lower() == city.lower()
    ].copy()

    if city_df.empty:
        return {
            "status": "error",
            "message": f"No data is available for {city}."
        }

    hourly_counts = (
        city_df["Hour"]
        .value_counts()
        .reindex(range(24), fill_value=0)
    )

    selected_count = int(hourly_counts.loc[hour])
    average_count = float(hourly_counts.mean())

    pattern_level = calculate_pattern_level(
        selected_count,
        average_count
    )

    recommendations = get_time_based_recommendations(hour)

    if crime_type:
        recommendations.extend(
            get_crime_specific_recommendations(crime_type)
        )

    recommendations.extend(get_general_safety_tips()[:2])

    recommendations = list(dict.fromkeys(recommendations))

    city_stats = get_city_statistics(df, city)

    return {
        "status": "success",
        "city": city,
        "selected_hour": hour,
        "time_period": get_time_period(hour),
        "historical_crime_count": selected_count,
        "average_hourly_count": round(average_count, 2),
        "pattern_level": pattern_level,
        "city_statistics": city_stats,
        "recommendations": recommendations
    }
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_crime_distribution_chart(
    city_df: pd.DataFrame,
    top_n: int = 10,
) -> go.Figure:
    """Create a horizontal bar chart of the most common crime types."""

    crime_counts = (
        city_df["Crime Description"]
        .value_counts()
        .head(top_n)
        .sort_values()
        .reset_index()
    )

    crime_counts.columns = [
        "Crime Description",
        "Crime Count",
    ]

    figure = px.bar(
        crime_counts,
        x="Crime Count",
        y="Crime Description",
        orientation="h",
        title="Top Crime Categories",
        labels={
            "Crime Count": "Recorded Crimes",
            "Crime Description": "Crime Type",
        },
    )

    figure.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
    )

    return figure


def create_hourly_crime_chart(
    city_df: pd.DataFrame,
) -> go.Figure:
    """Create an hourly crime trend line chart."""

    hourly_counts = (
        city_df.groupby("Hour")
        .size()
        .reindex(range(24), fill_value=0)
        .reset_index(name="Crime Count")
    )

    figure = px.line(
        hourly_counts,
        x="Hour",
        y="Crime Count",
        markers=True,
        title="Crime Activity by Hour",
        labels={
            "Hour": "Hour of Day",
            "Crime Count": "Recorded Crimes",
        },
    )

    figure.update_xaxes(
        tickmode="linear",
        tick0=0,
        dtick=2,
    )

    figure.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
    )

    return figure


def create_day_crime_chart(
    city_df: pd.DataFrame,
) -> go.Figure:
    """Create a bar chart showing crimes by day of the week."""

    day_order = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    day_counts = (
        city_df["DayOfWeek"]
        .value_counts()
        .reindex(day_order, fill_value=0)
        .reset_index()
    )

    day_counts.columns = [
        "Day",
        "Crime Count",
    ]

    figure = px.bar(
        day_counts,
        x="Day",
        y="Crime Count",
        title="Crime Activity by Day",
        labels={
            "Day": "Day of Week",
            "Crime Count": "Recorded Crimes",
        },
    )

    figure.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=55, b=20),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
    )

    return figure


def create_weapon_distribution_chart(
    city_df: pd.DataFrame,
    top_n: int = 8,
) -> go.Figure:
    """Create a donut chart of the most frequently recorded weapons."""

    weapon_counts = (
        city_df["Weapon Used"]
        .fillna("Unknown")
        .value_counts()
        .head(top_n)
        .reset_index()
    )

    weapon_counts.columns = [
        "Weapon",
        "Crime Count",
    ]

    figure = px.pie(
        weapon_counts,
        names="Weapon",
        values="Crime Count",
        hole=0.55,
        title="Weapon Distribution",
    )

    figure.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=55, b=20),
        paper_bgcolor="white",
        legend_title_text="Weapon",
    )

    return figure
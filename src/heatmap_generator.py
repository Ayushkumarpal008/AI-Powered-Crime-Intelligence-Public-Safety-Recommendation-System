from pathlib import Path

import folium
import pandas as pd
from folium.plugins import HeatMap


CITY_COORDINATES = {
    "Delhi": {
        "latitude": 28.6139,
        "longitude": 77.2090
    },
    "Ghaziabad": {
        "latitude": 28.6692,
        "longitude": 77.4538
    },
    "Faridabad": {
        "latitude": 28.4089,
        "longitude": 77.3178
    }
}


def add_city_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add approximate city-centre latitude and longitude values.
    """
    result = df.copy()

    result["Latitude"] = result["City"].map(
        lambda city: CITY_COORDINATES.get(city, {}).get("latitude")
    )

    result["Longitude"] = result["City"].map(
        lambda city: CITY_COORDINATES.get(city, {}).get("longitude")
    )

    return result


def get_city_map_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return city-level crime counts with coordinates.
    """
    city_counts = (
        df.groupby("City")
        .size()
        .reset_index(name="CrimeCount")
    )

    city_counts["Latitude"] = city_counts["City"].map(
        lambda city: CITY_COORDINATES.get(city, {}).get("latitude")
    )

    city_counts["Longitude"] = city_counts["City"].map(
        lambda city: CITY_COORDINATES.get(city, {}).get("longitude")
    )

    city_counts = city_counts.dropna(
        subset=["Latitude", "Longitude"]
    )

    return city_counts


def create_city_marker_map(df: pd.DataFrame) -> folium.Map:
    """
    Create a map showing crime counts for each NCR city.
    """
    city_data = get_city_map_data(df)

    crime_map = folium.Map(
        location=[28.61, 77.30],
        zoom_start=9,
        tiles="CartoDB positron"
    )

    for _, row in city_data.iterrows():
        popup_text = (
            f"<b>{row['City']}</b><br>"
            f"Recorded crimes: {row['CrimeCount']}"
        )

        folium.CircleMarker(
            location=[
                row["Latitude"],
                row["Longitude"]
            ],
            radius=max(8, row["CrimeCount"] / 300),
            popup=folium.Popup(
                popup_text,
                max_width=250
            ),
            tooltip=row["City"],
            fill=True,
            fill_opacity=0.65
        ).add_to(crime_map)

    return crime_map


def create_city_heatmap(df: pd.DataFrame) -> folium.Map:
    """
    Create a city-level heatmap using total crime counts.
    """
    city_data = get_city_map_data(df)

    crime_map = folium.Map(
        location=[28.61, 77.30],
        zoom_start=9,
        tiles="CartoDB dark_matter"
    )

    heat_data = city_data[
        ["Latitude", "Longitude", "CrimeCount"]
    ].values.tolist()

    HeatMap(
        heat_data,
        radius=45,
        blur=30,
        min_opacity=0.4
    ).add_to(crime_map)

    return crime_map


def save_map(
    crime_map: folium.Map,
    output_path: str | Path
) -> None:
    """
    Save a Folium map as an HTML file.
    """
    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    crime_map.save(str(output_path))
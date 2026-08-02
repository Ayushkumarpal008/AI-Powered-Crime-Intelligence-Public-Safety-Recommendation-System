from pathlib import Path
import sys

import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.data_preprocessing import prepare_crime_data
from src.feature_engineering import engineer_features
from src.crime_analysis import get_city_summary
from src.heatmap_generator import (
    create_city_marker_map,
    create_city_heatmap,
)
from src.crime_intelligence import CrimeIntelligenceEngine
from src.report_generator import generate_safety_report_pdf

from components.charts import (
    create_crime_distribution_chart,
    create_hourly_crime_chart,
    create_day_crime_chart,
    create_weapon_distribution_chart,
)


DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "crime_dataset_india.csv"
)


st.set_page_config(
    page_title="Crime Intelligence & Public Safety System",
    page_icon="🛡️",
    layout="wide",
)


st.markdown(
    """
    <style>
        /* Main page background */
        .stApp {
            background-color: #f4f7fb;
        }

        /* Reduce extra space at the top */
        .block-container {
            padding-top: 4rem;
            padding-bottom: 2rem;
        }

        /* Government-style header */
        .government-header {
            background: linear-gradient(
                135deg,
                #0b3d6e,
                #155a91
            );
            padding: 24px 30px;
            border-radius: 10px;
            margin-top: 8px;
            margin-bottom: 22px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
        }

        .government-header h1 {
            color: white;
            margin: 0;
            font-size: 30px;
            font-weight: 700;
        }

        .government-header p {
            color: #dcecff;
            margin-top: 8px;
            margin-bottom: 0;
            font-size: 16px;
        }

        /* Metric cards */
        div[data-testid="stMetric"] {
            background-color: white;
            border: 1px solid #d7e0ea;
            border-left: 5px solid #155a91;
            padding: 16px;
            border-radius: 8px;
            box-shadow: 0 2px 7px rgba(0, 0, 0, 0.06);
        }

        div[data-testid="stMetricLabel"] {
            color: #30475e;
            font-weight: 600;
        }

        div[data-testid="stMetricValue"] {
            color: #0b3d6e;
            font-weight: 700;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #eaf1f8;
            border-right: 1px solid #c9d6e3;
        }

        section[data-testid="stSidebar"] h2 {
            color: #0b3d6e;
        }

        /* Tab styling */
        button[data-baseweb="tab"] {
            font-weight: 600;
        }

        /* Section headings */
        h2, h3 {
            color: #123f68;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data() -> pd.DataFrame:
    """
    Load, clean, and engineer the Delhi NCR crime dataset.
    """
    df = prepare_crime_data(DATA_PATH)
    df = engineer_features(df)

    return df


def main() -> None:
    st.markdown(
        """
    <div class="government-header">
        <h1>AI-Powered Crime Intelligence & Public Safety Recommendation System</h1>
        <p>
            Delhi NCR crime analytics, interactive heatmaps,
            historical risk assessment and public safety guidance.
        </p>
    </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        df = load_data()
        engine = CrimeIntelligenceEngine(df)
    except FileNotFoundError:
        st.error(f"Dataset not found at: {DATA_PATH}")
        return
    except Exception as error:
        st.error(f"Unable to load the dataset: {error}")
        return

    st.sidebar.markdown(
        """
        <h2 style="color:#0B3D6E; margin-bottom:4px;">
            Analysis Filters
        </h2>
        <p style="color:#52677A; font-size:14px; margin-top:0;">
            Select a city to explore its historical crime patterns.
        </p>
        """,
        unsafe_allow_html=True,
    )

    city_options = sorted(df["City"].dropna().unique())

    selected_city = st.sidebar.selectbox(
        "Select city",
        city_options,
    )

    st.sidebar.divider()

    st.sidebar.caption(
        "Data shown in this dashboard is based on the available "
        "historical Delhi NCR crime dataset."
    )

    city_df = df[df["City"] == selected_city].copy()

    total_crimes = len(city_df)
    unique_crimes = city_df["Crime Description"].nunique()
    closed_cases = int(city_df["IsCaseClosed"].sum())

    closure_rate = (
        closed_cases / total_crimes * 100
        if total_crimes > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Recorded Crimes",
        f"{total_crimes:,}",
    )

    col2.metric(
        "Crime Categories",
        unique_crimes,
    )

    col3.metric(
        "Closed Cases",
        f"{closed_cases:,}",
    )

    col4.metric(
        "Closure Rate",
        f"{closure_rate:.2f}%",
    )

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Crime Analytics",
            "Crime Heatmap",
            "Risk Assessment & Safety",
            "City Summary",
        ]
    )

    with tab1:
        st.subheader(f"Crime Overview: {selected_city}")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.plotly_chart(
                create_crime_distribution_chart(city_df),
                use_container_width=True,
            )

        with chart_col2:
            st.plotly_chart(
                create_hourly_crime_chart(city_df),
                use_container_width=True,
            )

        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            st.plotly_chart(
                create_day_crime_chart(city_df),
                use_container_width=True,
            )

        with chart_col4:
            st.plotly_chart(
                create_weapon_distribution_chart(city_df),
                use_container_width=True,
            )

        st.subheader("Crime Records")

        st.dataframe(
            city_df[
                [
                    "Date of Occurrence",
                    "Time of Occurrence",
                    "City",
                    "Crime Description",
                    "Victim Age",
                    "Victim Gender",
                    "Weapon Used",
                    "Case Closed",
                ]
            ].head(100),
            use_container_width=True,
        )

    with tab2:
        st.subheader("Delhi NCR Crime Map")

        map_type = st.radio(
            "Choose map type",
            ["Marker Map", "Heatmap"],
            horizontal=True,
        )

        if map_type == "Marker Map":
            crime_map = create_city_marker_map(df)
        else:
            crime_map = create_city_heatmap(df)

        st_folium(
            crime_map,
            width=None,
            height=550,
            use_container_width=True,
        )

        st.info(
            "The map uses approximate city-centre coordinates. "
            "It represents city-level crime frequency, not exact crime locations."
        )

    with tab3:
        st.subheader("Public Safety Risk Assessment")

        day_options = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        selected_day = st.selectbox(
            "Select travel day",
            day_options,
        )

        selected_hour = st.slider(
            "Select travel hour",
            min_value=0,
            max_value=23,
            value=18,
        )

        if st.button(
            "Calculate Risk Score",
            type="primary",
        ):
            try:
                risk_result = engine.calculate_risk_score(
                    city=selected_city,
                    day=selected_day,
                    hour=selected_hour,
                )

                recommendations = (
                    engine.generate_safety_recommendations(
                        risk_result
                    )
                )
                pdf_bytes = generate_safety_report_pdf(
                    risk_result=risk_result,
                    recommendations=recommendations,
                )

                risk_score = risk_result["RiskScore"]
                risk_level = risk_result["RiskLevel"]

                st.metric(
                    "Relative Historical Risk Score",
                    f"{risk_score}/100",
                )

                if risk_level == "High":
                    st.error(f"Risk Level: {risk_level}")

                elif risk_level == "Medium":
                    st.warning(f"Risk Level: {risk_level}")

                else:
                    st.success(f"Risk Level: {risk_level}")

                st.caption(
                    "This score represents relative historical risk "
                    "within the available dataset. It does not guarantee "
                    "that an area is safe or unsafe."
                )

                st.subheader("Safety Recommendations")

                for number, recommendation in enumerate(
                    recommendations,
                    start=1,
                ):
                    st.write(
                        f"{number}. {recommendation}"
                    )
                report_file_name = (
                    f"safety_report_"
                    f"{selected_city.lower().replace(' ', '_')}_"
                    f"{selected_day.lower()}_"
                    f"{selected_hour:02d}00.pdf"
                )

                st.download_button(
                    label="Download Safety Report",
                    data=pdf_bytes,
                    file_name=report_file_name,
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True,
                )

            except ValueError as error:
                st.error(str(error))

            except KeyError as error:
                st.error(
                    f"Unable to calculate risk because data is "
                    f"missing for: {error}"
                )

    with tab4:
        st.subheader("Delhi NCR City Summary")

        summary = get_city_summary(df)

        st.dataframe(
            summary,
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
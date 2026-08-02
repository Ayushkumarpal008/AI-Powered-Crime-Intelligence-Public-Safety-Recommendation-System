"""
Crime Intelligence Module

This module provides:
1. City-wise risk score calculation
2. Dynamic public safety risk score
3. AI safety recommendations
"""

import numpy as np
import pandas as pd


class CrimeIntelligenceEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

        self.city_lookup = {}
        self.hour_lookup = {}
        self.day_lookup = {}

        self._prepare_lookup_tables()

    def _prepare_lookup_tables(self):
        """
        Prepare lookup dictionaries used by
        the Risk Score Engine.
        """

    
        # City Risk
        

        city_summary = (
            self.df.groupby("City")
            .size()
            .reset_index(name="CrimeCount")
        )

        city_summary["LogCrime"] = np.log1p(
            city_summary["CrimeCount"]
        )

        minimum = city_summary["LogCrime"].min()
        maximum = city_summary["LogCrime"].max()

        city_summary["RiskScore"] = (
            (city_summary["LogCrime"] - minimum)
            / (maximum - minimum)
            * 100
        )

        self.city_lookup = (
            city_summary
            .set_index("City")["RiskScore"]
            .to_dict()
        )

        
        # Hour Risk
        

        hour_summary = (
            self.df.groupby("Hour")
            .size()
            .reset_index(name="CrimeCount")
        )

        minimum = hour_summary["CrimeCount"].min()
        maximum = hour_summary["CrimeCount"].max()

        hour_summary["RiskScore"] = (
            (hour_summary["CrimeCount"] - minimum)
            / (maximum - minimum)
            * 100
        )

        self.hour_lookup = (
            hour_summary
            .set_index("Hour")["RiskScore"]
            .to_dict()
        )

        
        # Day Risk
        

        day_summary = (
            self.df.groupby("DayOfWeek")
            .size()
            .reset_index(name="CrimeCount")
        )

        day_order = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

        day_summary["DayOfWeek"] = pd.Categorical(
            day_summary["DayOfWeek"],
            categories=day_order,
            ordered=True,
        )

        day_summary = day_summary.sort_values("DayOfWeek")

        minimum = day_summary["CrimeCount"].min()
        maximum = day_summary["CrimeCount"].max()

        day_summary["RiskScore"] = (
            (day_summary["CrimeCount"] - minimum)
            / (maximum - minimum)
            * 100
        )

        self.day_lookup = (
            day_summary
            .set_index("DayOfWeek")["RiskScore"]
            .to_dict()
        )

    def calculate_risk_score(
        self,
        city: str,
        day: str,
        hour: int,
    ):

        city_score = self.city_lookup[city]
        hour_score = self.hour_lookup[hour]
        day_score = self.day_lookup[day]

        night_score = 100 if hour >= 20 or hour <= 5 else 0

        final_score = (
            city_score * 0.40
            + hour_score * 0.30
            + day_score * 0.20
            + night_score * 0.10
        )

        final_score = round(final_score, 2)

        if final_score >= 70:
            level = "High"
        elif final_score >= 40:
            level = "Medium"
        else:
            level = "Low"

        return {
            "RiskScore": final_score,
            "RiskLevel": level,
            "City": city,
            "Day": day,
            "Hour": hour,
        }

    def generate_safety_recommendations(
        self,
        risk_result: dict,
    ):

        level = risk_result["RiskLevel"]
        hour = risk_result["Hour"]

        recommendations = []

        if level == "High":

            recommendations.extend([
                "Avoid travelling alone.",
                "Prefer well-lit roads.",
                "Share your live location.",
                "Use verified transport.",
                "Keep emergency contacts ready.",
            ])

        elif level == "Medium":

            recommendations.extend([
                "Stay alert.",
                "Avoid isolated streets.",
                "Keep your phone charged.",
                "Inform someone about your route.",
            ])

        else:

            recommendations.extend([
                "Follow normal safety precautions.",
                "Remain aware of your surroundings.",
            ])

        if hour >= 20 or hour <= 5:

            recommendations.extend([
                "Avoid poorly lit areas.",
                "Travel with a companion if possible.",
            ])

        recommendations = list(dict.fromkeys(recommendations))

        return recommendations
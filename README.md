# 🛡️ AI-Powered Crime Intelligence & Public Safety Recommendation System

An end-to-end Data Analytics project that analyzes historical crime patterns across Delhi NCR using Python, Pandas, Plotly, Folium, and Streamlit. The system provides interactive crime analytics, location-based crime visualization, historical risk assessment, public safety recommendations, and downloadable PDF safety reports through an interactive dashboard.

---

## 🚀 Features

- Interactive Crime Analytics Dashboard
- Crime Heatmap & Marker Map
- Historical Risk Score Calculation
- Public Safety Recommendations
- Downloadable PDF Safety Report
- City-wise Crime Analysis
- Interactive Plotly Visualizations
- Historical Crime Pattern Analysis

---

## 🤖 Risk Assessment Engine

The project includes an intelligent Risk Assessment Engine that evaluates the historical crime risk of a selected city based on the travel day and travel hour. It calculates a relative risk score, classifies the location into Low, Medium, or High risk, and generates context-based public safety recommendations. Users can also download a detailed PDF safety report directly from the dashboard.

---
## 🛠 Tech Stack

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Folium
- Streamlit Folium
- ReportLab

---

## 📂 Project Structure

```text
AI Public Crime Heatmap/
│
├── .streamlit/
│   └── config.toml                     # Streamlit theme configuration (colors, fonts, UI settings)
│
├── .vscode/
│   └── settings.json                   # VS Code workspace settings
│
├── app/
│   ├── components/
│   │   ├── charts.py                   # Plotly chart functions used in the dashboard
│   │   └── sidebar.py                  # Sidebar UI components (if used)
│   │
│   └── app.py                          # Main Streamlit dashboard application
│
├── data/
│   ├── external/                       # External datasets (reserved for future use)
│   ├── processed/                      # Cleaned and processed datasets
│   └── raw/
│       └── crime_dataset_india.csv     # Original historical crime dataset
│
├── models/
│   └── .gitkeep                        # Keeps the models folder in Git (reserved for future ML models)
│
├── notebooks/
│   ├── 01_data_exploration.ipynb       # Initial dataset exploration
│   ├── 02_data_cleaning.ipynb          # Data cleaning and preprocessing
│   ├── 03_feature_engineering.ipynb    # Feature engineering and feature creation
│   ├── 04_exploratory_data_analysis.ipynb # Data visualization and EDA
│   ├── 05_model_experiments.ipynb      # Model experiments and evaluation
│   └── 06_crime_intelligence.ipynb     # Development of the Crime Intelligence Engine
│
├── reports/
│   ├── figures/                        # Generated figures and visual outputs
│   ├── project_report.md               # Automatically generated project report
│   └── test_safety_report.pdf          # Sample generated PDF safety report
│
├── src/
│   ├── __init__.py                     # Marks src as a Python package
│   ├── crime_analysis.py               # Crime analytics and city summary functions
│   ├── crime_intelligence.py           # Risk score calculation and intelligence engine
│   ├── data_preprocessing.py           # Dataset loading and preprocessing
│   ├── feature_engineering.py          # Feature engineering utilities
│   ├── heatmap_generator.py            # Folium heatmap and marker map generation
│   ├── report_generator.py             # PDF safety report generation
│   ├── safety_recommendation.py        # Public safety recommendation engine
│   ├── time_pattern_analysis.py        # Day-wise and hour-wise crime pattern analysis
│   └── utils.py                        # Common helper functions
│
├── tests/
│   └── test_crime_intelligence.py      # Backend testing for the Crime Intelligence Engine
│
├── .gitignore                          # Git ignored files and folders
├── main.py                             # Project entry point (if required)
├── README.md                           # Project documentation
└── requirements.txt                    # Python project dependencies
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Ayushkumarpal008/AI-Powered-Crime-Intelligence-Public-Safety-Recommendation-System.git
```

Move into the project folder

```bash
cd AI-Powered-Crime-Intelligence-Public-Safety-Recommendation-System
```

Install the required dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Launch the Streamlit application

```bash
streamlit run app/app.py
```

Run the backend test

```bash
python tests/test_crime_intelligence.py
```

---

## 📈 Outputs

- Interactive Crime Analytics Dashboard
- Crime Heatmap & Marker Map
- Historical Risk Score
- Public Safety Recommendations
- Downloadable PDF Safety Report
- City-wise Crime Summary

---

## 🔮 Future Improvements

- Real-time crime data integration
- Multi-city support
- Mobile application
- Live emergency alert system

---

## 🚀 Live Demo

[👉 Open Live Project] https://ai-healthcare-insurance-fraud-detection-system-8bn6eqwxq7bfd3m.streamlit.app/

## 👨‍💻 Author

**Ayush Kumar Pal**

B.Tech – Computer Science & Data Science

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent

if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from pathlib import Path

from src.data_preprocessing import prepare_crime_data
from src.feature_engineering import engineer_features
from src.crime_intelligence import CrimeIntelligenceEngine

from src.report_generator import generate_safety_report_pdf


project_root = Path(__file__).resolve().parent.parent

data_path = (
    project_root
    / "data"
    / "raw"
    / "crime_dataset_india.csv"
)

df = prepare_crime_data(data_path)
df = engineer_features(df)

engine = CrimeIntelligenceEngine(df)

risk_result = engine.calculate_risk_score(
    city="Delhi",
    day="Wednesday",
    hour=1,
)

recommendations = engine.generate_safety_recommendations(
    risk_result
)

print("Risk Result:")
print(risk_result)

print("\nSafety Recommendations:")

for number, recommendation in enumerate(
    recommendations,
    start=1,
):
    print(f"{number}. {recommendation}")

pdf_bytes = generate_safety_report_pdf(
    risk_result=risk_result,
    recommendations=recommendations,
)

report_path = (
    project_root
    / "reports"
    / "test_safety_report.pdf"
)

report_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

report_path.write_bytes(pdf_bytes)

print(f"\nPDF report saved to: {report_path}")
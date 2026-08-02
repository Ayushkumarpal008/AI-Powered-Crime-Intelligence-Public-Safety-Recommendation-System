"""
PDF Safety Report Generator

Creates a downloadable public-safety report containing:
- Selected city, day, and hour
- Relative historical risk score
- Risk level
- Safety recommendations
- Important disclaimer
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generate_safety_report_pdf(
    risk_result: dict,
    recommendations: list[str],
) -> bytes:
    """
    Generate a public-safety PDF report and return it as bytes.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="Public Safety Risk Assessment Report",
        author="AI-Powered Crime Intelligence System",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#0B3D6E"),
        spaceAfter=10,
    )

    subtitle_style = ParagraphStyle(
        name="ReportSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#52677A"),
        spaceAfter=18,
    )

    heading_style = ParagraphStyle(
        name="SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0B3D6E"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        name="ReportNormal",
        parent=styles["Normal"],
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#243447"),
    )

    disclaimer_style = ParagraphStyle(
        name="Disclaimer",
        parent=styles["Normal"],
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#5F6B76"),
        backColor=colors.HexColor("#EEF3F8"),
        borderColor=colors.HexColor("#CAD6E2"),
        borderWidth=0.5,
        borderPadding=8,
        spaceBefore=18,
    )

    risk_score = risk_result["RiskScore"]
    risk_level = risk_result["RiskLevel"]
    city = risk_result["City"]
    day = risk_result["Day"]
    hour = risk_result["Hour"]

    if risk_level == "High":
        risk_color = colors.HexColor("#B42318")
    elif risk_level == "Medium":
        risk_color = colors.HexColor("#B7791F")
    else:
        risk_color = colors.HexColor("#16794B")

    story = []

    story.append(
        Paragraph(
            "AI-Powered Crime Intelligence & Public Safety Recommendation System",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Relative Historical Public Safety Risk Assessment Report",
            subtitle_style,
        )
    )

    summary_data = [
        ["Location", city],
        ["Travel Day", day],
        ["Travel Hour", f"{hour:02d}:00"],
        ["Risk Score", f"{risk_score:.2f} / 100"],
        ["Risk Level", risk_level],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[50 * mm, 100 * mm],
    )

    summary_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#E8F0F7"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (0, -1),
                    colors.HexColor("#0B3D6E"),
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (0, -1),
                    "Helvetica-Bold",
                ),
                (
                    "FONTNAME",
                    (1, 0),
                    (1, -2),
                    "Helvetica",
                ),
                (
                    "FONTNAME",
                    (1, -1),
                    (1, -1),
                    "Helvetica-Bold",
                ),
                (
                    "TEXTCOLOR",
                    (1, -1),
                    (1, -1),
                    risk_color,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#CBD5E1"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
            ]
        )
    )

    story.append(summary_table)
    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph(
            "Safety Recommendations",
            heading_style,
        )
    )

    for number, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        story.append(
            Paragraph(
                f"{number}. {recommendation}",
                normal_style,
            )
        )
        story.append(Spacer(1, 2.5 * mm))

    story.append(
        Paragraph(
            (
                "<b>Important disclaimer:</b> This report is based on "
                "relative patterns found in the available historical dataset. "
                "It does not provide real-time crime information and does not "
                "guarantee that a location is safe or unsafe. Users should "
                "continue following official public-safety guidance and use "
                "their own judgement."
            ),
            disclaimer_style,
        )
    )

    document.build(story)

    pdf_bytes = buffer.getvalue()
    buffer.close()

    return pdf_bytes
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def create_prediction_pdf(record):
    buffer = BytesIO()
    page = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 70

    page.setTitle(f"EcoMind AI Report {record.id}")
    page.setFont("Helvetica-Bold", 20)
    page.drawString(55, y, "EcoMind AI - Waste Analysis Report")
    y -= 45

    page.setFont("Helvetica", 11)
    rows = [
        f"Prediction ID: {record.id}",
        f"File: {record.filename}",
        f"Detected category: {record.category.title()}",
        f"Confidence: {record.confidence * 100:.2f}%",
        f"Date: {record.created_at}",
        "",
        "Disposal recommendation:",
        record.disposal_advice,
        "",
        "Environmental impact estimate:",
        record.impact_estimate,
        "",
        "Note: Impact values are illustrative educational estimates, not measured lifecycle results."
    ]
    for row in rows:
        if y < 70:
            page.showPage()
            y = height - 70
            page.setFont("Helvetica", 11)
        page.drawString(55, y, row[:110])
        y -= 22

    page.save()
    buffer.seek(0)
    return buffer.getvalue()

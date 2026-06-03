import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reports.models import Report
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import mm


# Function to generate the PDF
def generate_pdf(report: Report):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('Inter', 'Inter.ttf'))
    story = []
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    style = ParagraphStyle(
        'Inter',
        fontSize=11,
        leading=13,
        leftIndent=15*mm,
        rightIndent=15*mm,
        spaceAfter=8*mm
    )

    text = f"""{report.datetime} в районе {report.address} ({report.lat}, {report.lon}) водитель автомобиля с госномером {report.gosnomer} совершил нарушение: {report.violation}. {report.description}
Прошу привлечь нарушителя к ответственности.
""" 
    story.append(Paragraph(text, style))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Заявитель: _____________________", style))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(f"Дата: {datetime.datetime.now()}", style))

    doc.build(story)
    buffer.seek(0)
    return buffer

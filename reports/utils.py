import datetime
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import KeepTogether, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import mm

from reports.schemas import ReportFull


# Function to generate the PDF
def generate_pdf(report: ReportFull):
    buffer = BytesIO()
    pdfmetrics.registerFont(TTFont('Inter', 'fonts/Inter.ttf'))
    story = []
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    style = ParagraphStyle(
        'Inter',
        fontName='Inter',
        fontSize=11,
        leading=13,
        leftIndent=15*mm,
        rightIndent=15*mm,
        spaceAfter=8*mm
    )

    story.append(Paragraph("Заявление", style))
    story.append(Spacer(1, 2*mm))

    text = f"""{report.datetime} в районе {report.address} ({report.lat}, {report.lon}) водитель автомобиля с госномером {report.gosnomer} совершил нарушение: {report.violation}. {report.description}""" 
    story.append(Paragraph(text, style))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph('Прошу привлечь нарушителя к ответственности.', style))
    for image in report.assets:
        img_data = open(image.uri, "rb").read()
        img = KeepTogether(Image(BytesIO(img_data), width=10*mm))
        story.append(img)
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph("Заявитель: _____________________", style))
    story.append(Spacer(1, 2*mm))
    story.append(Paragraph(f"Дата: {datetime.datetime.now()}", style))

    doc.build(story)
    buffer.seek(0)
    return buffer

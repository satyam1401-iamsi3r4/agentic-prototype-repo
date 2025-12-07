import io, datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_sanction_pdf(name: str, amount: int, roi: float, tenure: int, credit_score: int) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 80, "Tata Capital - Personal Loan Sanction Letter")
    c.setFont("Helvetica", 11)
    y = height - 120
    lines = [
        f"Name: {name}",
        f"Loan Amount Approved: INR {amount}",
        f"Rate of Interest (p.a.): {roi}%",
        f"Tenure: {tenure} months",
        f"Credit Score: {credit_score}",
        "",
        "This is a system generated sanction letter.",
        f"Date: {datetime.date.today().isoformat()}"
    ]
    for line in lines:
        c.drawString(50, y, line)
        y -= 18
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()

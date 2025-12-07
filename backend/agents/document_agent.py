from ..utils.pdf_generator import generate_sanction_pdf

async def create_sanction_pdf(session):
    pdf_bytes = generate_sanction_pdf(
        name=session.get('name','User'),
        amount=session['offer']['eligible_amount'],
        roi=session['offer']['roi'],
        tenure=session['offer']['tenure'],
        credit_score=session['credit']['score']
    )
    return pdf_bytes

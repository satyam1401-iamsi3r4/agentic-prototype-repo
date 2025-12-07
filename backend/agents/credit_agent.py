def mock_credit_score(pan: str or None, name: str or None):
    base = 700
    if pan and len(pan) >= 3:
        base += 30
    if name and name.lower() and name.lower()[0] in "abcdefghijklm":
        base += 10
    return {"score": base, "risk_category": "low" if base >= 720 else "medium"}

async def run_credit(pan: str, name: str):
    return mock_credit_score(pan, name)

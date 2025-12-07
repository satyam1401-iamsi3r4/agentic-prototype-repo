def mock_kyc_lookup(aadhaar: str or None, name: str):
    score = 90 if aadhaar and len(aadhaar) % 2 == 0 else 75
    return {
        "status": "verified" if score >= 80 else "partial",
        "name": name,
        "dob": "1995-01-01",
        "address": "Sample Address, City",
        "kyc_score": score
    }

async def run_kyc(aadhaar: str, name: str):
    return mock_kyc_lookup(aadhaar, name)

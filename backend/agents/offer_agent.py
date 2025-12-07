def calculate_offer(monthly_income: int, credit_score: int, requested_amount: int or None = None):
    max_loan = monthly_income * 6
    if credit_score >= 750:
        roi = 9.5
        multiplier = 8
    elif credit_score >= 700:
        roi = 10.5
        multiplier = 6
    else:
        roi = 13.0
        multiplier = 4
    eligible = min(max_loan * multiplier // 6, requested_amount or (max_loan * multiplier // 6))
    tenure = 36 if eligible <= 300000 else 60
    return {"eligible_amount": int(eligible), "roi": roi, "tenure": tenure}

async def run_offer(monthly_income: int, credit_score: int, requested_amount: int or None):
    return calculate_offer(monthly_income, credit_score, requested_amount)

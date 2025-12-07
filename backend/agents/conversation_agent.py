# conversation_agent.py
# Minimal orchestrator agent. In production, use LLM to decide next_action.
async def decide_next_action(session):
    # Returns a dict: {'next_action': <action>, 'reply': <text>}
    if 'name' not in session:
        return {'next_action': 'collect_name', 'reply': "Hi — I'm Tata Capital AI Assistant. What's your full name?"}
    if 'monthly_income' not in session:
        return {'next_action': 'collect_income', 'reply': "What's your monthly income (in INR)?"}
    if not session.get('kyc_done'):
        return {'next_action': 'do_kyc', 'reply': "Please provide Aadhaar for quick KYC or type 'skip'."}
    if not session.get('credit_done'):
        return {'next_action': 'do_credit', 'reply': "Please provide PAN for credit check or type 'skip'."}
    if 'requested_amount' not in session:
        return {'next_action': 'offer', 'reply': "Enter requested loan amount (numbers only)."}
    if session.get('offer') and not session.get('sanction_generated'):
        return {'next_action': 'idle', 'reply': "Type 'accept' to generate a sanction letter or 'decline'."}
    return {'next_action': 'idle', 'reply': "Session complete."}

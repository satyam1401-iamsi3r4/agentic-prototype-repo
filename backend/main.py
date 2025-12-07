import os, json, uuid, base64
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import aioredis
from pydantic import BaseModel
from agents import conversation_agent, kyc_agent, credit_agent, offer_agent, document_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
redis = None

@app.on_event('startup')
async def startup():
    global redis
    redis = aioredis.from_url(REDIS_URL, encoding='utf-8', decode_responses=True)

@app.on_event('shutdown')
async def shutdown():
    global redis
    if redis:
        await redis.close()

async def save_session(session_id: str, session_obj: dict):
    await redis.set(f"session:{session_id}", json.dumps(session_obj), ex=60*60*6)

async def load_session(session_id: str):
    raw = await redis.get(f"session:{session_id}")
    return json.loads(raw) if raw else None

class ChatInput(BaseModel):
    user_id: str | None = None
    message: str
    session: dict | None = None

@app.get('/health')
async def health():
    return {"status":"ok"}

@app.post('/chat')
async def chat_endpoint(chat: ChatInput):
    session_id = chat.session.get('session_id') if chat.session else None
    if not session_id:
        session_id = str(uuid.uuid4())
        session = {'session_id': session_id}
    else:
        session = await load_session(session_id) or {'session_id': session_id}

    user_msg = chat.message.strip()

    # quick handlers
    if 'name' not in session and user_msg and user_msg.lower() != 'hi':
        session['name'] = user_msg
        await save_session(session_id, session)
        return JSONResponse({"reply": f"Nice to meet you, {session['name']}. What's your monthly income (in INR)?", "session": session})

    if 'monthly_income' not in session:
        digits = ''.join([c for c in user_msg if c.isdigit()])
        if digits:
            session['monthly_income'] = int(digits)
            await save_session(session_id, session)
            return JSONResponse({"reply": "Please provide your Aadhaar number (mock) for quick KYC check, or type 'skip'.", "session": session})
        else:
            return JSONResponse({"reply": "Please enter monthly income as a number.", "session": session})

    # use conversation agent to decide next action
    conv = await conversation_agent.decide_next_action(session)
    action = conv.get('next_action')

    # KYC step
    if action == 'do_kyc':
        if 'skip' in user_msg.lower():
            session['kyc'] = {'status': 'skipped'}
            session['kyc_done'] = True
            await save_session(session_id, session)
            return JSONResponse({"reply": "KYC skipped. Provide PAN (or type skip) to check credit score.", "session": session})
        kyc_res = await kyc_agent.run_kyc(user_msg.strip(), session.get('name'))
        session['kyc'] = kyc_res
        session['kyc_done'] = True
        await save_session(session_id, session)
        return JSONResponse({"reply": f"KYC status: {kyc_res['status']}. Now provide PAN (or type skip) for credit check.", "session": session})

    # Credit step
    if action == 'do_credit':
        if 'skip' in user_msg.lower():
            session['credit'] = {"score": 650, "risk_category": "medium"}
            session['credit_done'] = True
            await save_session(session_id, session)
            return JSONResponse({"reply": "Credit check skipped. Enter requested loan amount (numbers only).", "session": session})
        credit_res = await credit_agent.run_credit(user_msg.strip(), session.get('name'))
        session['credit'] = credit_res
        session['credit_done'] = True
        await save_session(session_id, session)
        return JSONResponse({"reply": f"Credit score: {credit_res['score']}. Enter requested loan amount (numbers only).", "session": session})

    # Offer step
    if action == 'offer':
        digits = ''.join([c for c in user_msg if c.isdigit()])
        if not digits:
            return JSONResponse({"reply": "Please enter the requested loan amount as a number.", "session": session})
        session['requested_amount'] = int(digits)
        offer = await offer_agent.run_offer(session['monthly_income'], session['credit']['score'], session['requested_amount'])
        session['offer'] = offer
        await save_session(session_id, session)
        return JSONResponse({"reply": f"We can offer ₹{offer['eligible_amount']} at {offer['roi']}% p.a. Tenure: {offer['tenure']} months. Type 'accept' to generate sanction letter or 'decline'.", "session": session})

    # Accept -> generate PDF
    if 'accept' in user_msg.lower() and session.get('offer') and not session.get('sanction_generated'):
        pdf_bytes = await document_agent.create_sanction_pdf(session)
        session['sanction_generated'] = True
        await save_session(session_id, session)
        b64 = base64.b64encode(pdf_bytes).decode('utf-8')
        return JSONResponse({"reply": "Sanction letter generated.", "pdf_base64": b64, "session": session})

    # fallback
    return JSONResponse({"reply": conv.get('reply', 'I did not understand that.'), "session": session})

# Agentic AI Loan Assistant - Prototype

This repository contains a prototype of an Agentic AI Loan Assistant (FastAPI backend + React frontend).

## Features
- Multi-agent orchestration (Conversation → KYC → Credit → Offer → Document)
- Redis-backed session persistence
- Tata Capital themed React UI
- Voice input (Web Speech API) and speech output
- PDF sanction letter generation
- Ready for deployment on Render (render.yaml included)

## Quick local run (dev)

### Backend
1. Start Redis locally (or use a cloud Redis)
2. python -m venv .venv
3. source .venv/bin/activate
4. pip install -r backend/requirements.txt
5. cd backend && uvicorn main:app --reload --port 8000

### Frontend
1. cd frontend
2. npm install
3. npm run dev

Set VITE_BACKEND_URL to your backend if needed.

## Deploy
This repo includes `render.yaml` to deploy on Render (backend, frontend, and managed Redis). See Render docs to connect your GitHub repo.

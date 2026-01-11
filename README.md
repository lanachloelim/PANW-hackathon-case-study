# How to run locally

## Backend (from repo root):
- Install deps:
```
pip install -r backend/requirements.txt
```
- Set your Together API key in the shell:
```
export TOGETHER_API_KEY="your_key_here"
```
- Start the API (run from the backend folder):
```
python3 server.py
```
- Server runs at http://localhost:8000

## Frontend (dashboard):
- Install and run (run from dashboard-ui folder):
```
npm install
npm run dev
```
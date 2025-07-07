import os
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth, OAuthError
from dotenv import load_dotenv
import httpx
from supabase import create_client, Client

load_dotenv()

CLIENT_ID     = os.getenv('QB_CLIENT_ID')
CLIENT_SECRET = os.getenv('QB_CLIENT_SECRET')
REALM_ID      = os.getenv('QB_REALM_ID')
REDIRECT_URI  = os.getenv('QB_REDIRECT_URI')
SUPABASE_URL  = os.getenv('SUPABASE_URL')
SUPABASE_KEY  = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

app = FastAPI(title="QuickBooks Proxy API")

oauth = OAuth()
oauth.register(
    name='qb',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url='https://oauth.platform.intuit.com/.well-known/openid_sandbox',
    client_kwargs={'scope': 'com.intuit.quickbooks.accounting'},
)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Simple in-memory store for demo; swap for Redis/session in prod
token_store = {}

@app.get("/login")
async def login(request: Request):
    return await oauth.qb.authorize_redirect(request, REDIRECT_URI)

@app.get("/auth")
async def auth(request: Request):
    try:
        token = await oauth.qb.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    token_store['access_token'] = token['access_token']
    return RedirectResponse(url="/docs")

@app.get("/api/qb/reports/aging")
async def get_aging_report():
    token = token_store.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    url = f"https://sandbox-quickbooks.api.intuit.com/v3/company/{REALM_ID}/reports/AgedReceivableDetail"
    params = {
        'report_date': '2025-06-30',
        'start_duedate': '2025-01-01',
        'end_duedate': '2025-06-30',
        'columns': 'due_date,cust_name'
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        # Upsert the report data into Supabase table "aging_reports"
        supabase.table('aging_reports').insert(data).execute()
        return data
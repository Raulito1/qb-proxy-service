from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        cursor_factory=RealDictCursor
    )

@app.get("/api/receivables")
def get_receivables():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM aged_receivable_detail ORDER BY due_date;")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return results
    except Exception as e:
        return {"error": str(e)}
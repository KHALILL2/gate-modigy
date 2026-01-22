import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
DB_FILE = "gate_access.db"

# Data model for the scan request
class ScanRequest(BaseModel):
    barcode: str

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT)")
        # Insert test IDs (using 2025 standard sample IDs)
        cursor.executemany("INSERT OR IGNORE INTO users VALUES (?,?)", 
                           [('6221000001390', 'yassen'), ('6223007356714', 'Guest'),('2120003','alaa')])
        conn.commit()

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/verify")
async def verify_id(request: ScanRequest):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM users WHERE id = ?", (request.barcode,))
        user = cursor.fetchone()
    
    if not user:
        raise HTTPException(status_code=403, detail="Access Denied: ID not found")
    
    return {"status": "success", "user": user[0]}

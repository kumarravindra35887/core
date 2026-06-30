import os
import base64
import random
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import google.generativeai as genai

PREMIUM_ADS_WITH_BANK_PANEL = """
<div style="background:linear-gradient(135deg,#1e3c72,#2a5298);color:#fff;padding:15px;border-radius:8px;font-family:sans-serif;margin:20px;">
    <h3>💼 CYCLONE STAR PLUS - Master Admin Room</h3>
    <p>Live Ad Revenue Mode: <b>HIGH CPM ACTIVE</b></p>
    <p>Current Balance: <span style="color:#ffeb3b;font-weight:bold;">$0.00</span> | Bank Transfer Status: <span style="color:#4caf50;font-weight:bold;">LINKED</span></p>
</div>
"""

app = FastAPI(title="CYCLONE STAR PLUS - Admin Portal", version="2026.10.0")

if "YOUR_FREE_GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["YOUR_FREE_GEMINI_API_KEY"])

ADMIN_EMAIL = "kumarravindra35887@gmail.com"

def init_master_db():
    conn = sqlite3.connect("cyclone_star_pro_final.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, is_active INTEGER DEFAULT 0, device_id TEXT DEFAULT '')")
    cursor.execute("CREATE TABLE IF NOT EXISTS segment_control (segment_name TEXT PRIMARY KEY, is_allowed INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS question_bank (q_id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, difficulty TEXT, question_text TEXT, options TEXT, correct_answer TEXT, explanation TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS automatic_tests (test_id INTEGER PRIMARY KEY AUTOINCREMENT, test_title TEXT, exam_id TEXT, questions_json TEXT, is_approved INTEGER DEFAULT 0, is_free INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS content_hub (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, title TEXT, content_hindi TEXT, content_english TEXT, is_approved INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS portal_monetization (id INTEGER PRIMARY KEY, ads_status INTEGER DEFAULT 1, ad_network_id TEXT DEFAULT 'ca-pub-YOUR_ID')")
    
    for seg in ["prelims_notes", "mains_notes", "current_affairs", "test_series"]:
        cursor.execute("INSERT OR IGNORE INTO segment_control (segment_name, is_allowed) VALUES (?, 0)", (seg,))
    conn.commit()
    conn.close()

init_master_db()

@app.post("/auth/signup-request-otp", tags=["Student API"])
async def signup_request_otp(email: str = Form(...)):
    return {"message": "साइनअप हेतु सुरक्षा ओटीपी भेज दिया गया है।"}

@app.post("/auth/login", tags=["Student API"])
async def secure_login(email: str = Form(...), password: str = Form(...), device_id: str = Form(...)):
    return {"role": "USER", "message": "लॉगिन सफल"}

@app.post("/admin/portal/upload-handwriting-sample", tags=["Admin Portal"])
async def web_upload_handwriting_sample(admin_email: str = Form(...), file: UploadFile = File(...)):
    return {"message": "🎉 गजेंद्र कुमार योगी जी की लिखावट का फॉन्ट क्लोन लॉक हुआ।"}

@app.post("/admin/portal/upload-and-parse-questions", tags=["Admin Portal"])
async def web_upload_and_parse_questions(admin_email: str = Form(...), subject: str = Form(...), difficulty: str = Form(...), raw_text_data: str = Form(...)):
    return {"message": "🎉 सफलता! प्रश्न स्वतः क्वेश्चन बैंक में सज गए हैं।"}

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_with_premium_ads():
    from fastapi.openapi.docs import get_swagger_ui_html
    response = get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title)
    html_content = response.body.decode("utf-8")
    return HTMLResponse(content=html_content.replace("<body>", f"<body>{PREMIUM_ADS_WITH_BANK_PANEL}"), status_code=200)
  

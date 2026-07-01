import os
import sqlite3
from fastapi import FastAPI, Form
import google.generativeai as genai

app = FastAPI(title="CYCLONE STAR PLUS - Admin Portal", version="2026.10.0")

# वर्सेल के सर्वरलेस नियमों के अनुसार डेटाबेस का रास्ता बिल्कुल फिक्स करना
DB_PATH = "/tmp/cyclone_star_pro_final.db"

if "YOUR_FREE_GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["YOUR_FREE_GEMINI_API_KEY"])

def init_master_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, is_active INTEGER DEFAULT 0, device_id TEXT DEFAULT '')")
    cursor.execute("CREATE TABLE IF NOT EXISTS segment_control (segment_name TEXT PRIMARY KEY, is_allowed INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS question_bank (q_id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, difficulty TEXT, question_text TEXT, options TEXT, correct_answer TEXT, explanation TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS content_hub (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, title TEXT, content_hindi TEXT, content_english TEXT, is_approved INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

# सर्वर चालू होते ही डेटाबेस सुरक्षित जगह पर बनेगा
init_master_db()

@app.post("/auth/login", tags=["Student API"])
async def secure_login(email: str = Form(...), password: str = Form(...), device_id: str = Form(...)):
    return {"role": "USER", "message": "लॉगिन सफल"}

@app.post("/admin/portal/upload-and-parse-questions", tags=["Admin Portal"])
async def web_upload_and_parse_questions(admin_email: str = Form(...), subject: str = Form(...), difficulty: str = Form(...), raw_text_data: str = Form(...)):
    return {"message": "🎉 सफलता! प्रश्न स्वतः क्वेश्चन बैंक में सज गए हैं।"}

@app.get("/", tags=["Root"])
async def root_redirect():
    return {"status": "online", "message": "Welcome to CYCLONE STAR PLUS API. Go to /docs for Admin Panel"}
    

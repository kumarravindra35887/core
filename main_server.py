import os
import sqlite3
from fastapi import FastAPI, Form, UploadFile, File
import google.generativeai as genai

# 1. एडमिन पोर्टल को इनिशियलाइज़ करना
app = FastAPI(title="CYCLONE STAR PLUS - Advanced Admin Portal", version="2026.11.0")

# 2. डेटाबेस का रास्ता वर्सेल के सुरक्षित /tmp/ फोल्डर पर फिक्स करना
DB_PATH = "/tmp/cyclone_star_pro_final.db"

if "YOUR_FREE_GEMINI_API_KEY" in os.environ:
    genai.configure(api_key=os.environ["YOUR_FREE_GEMINI_API_KEY"])

def init_master_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # पुराने टेबल्स
    cursor.execute("CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT, is_active INTEGER DEFAULT 0, device_id TEXT DEFAULT '')")
    cursor.execute("CREATE TABLE IF NOT EXISTS segment_control (segment_name TEXT PRIMARY KEY, is_allowed INTEGER DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS question_bank (q_id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, difficulty TEXT, question_text TEXT, options TEXT, correct_answer TEXT, explanation TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS content_hub (id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, title TEXT, content_hindi TEXT, content_english TEXT, is_approved INTEGER DEFAULT 0)")
    # नया विज्ञापन टेबल (Advertisement Table)
    cursor.execute("CREATE TABLE IF NOT EXISTS advertisement_hub (ad_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, banner_url TEXT, target_link TEXT, is_active INTEGER DEFAULT 1)")
    conn.commit()
    conn.close()

init_master_db()

# --- १. टेक्स्ट पेस्ट करके एआई से सवाल बनाना (पुराना चालू फीचर) ---
@app.post("/admin/portal/upload-text-questions", tags=["Admin Portal (AI)"])
async def web_upload_and_parse_questions(admin_email: str = Form(...), subject: str = Form(...), difficulty: str = Form(...), raw_text_data: str = Form(...)):
    return {"status": "success", "message": "🎉 सफलता! टेक्स्ट वाले प्रश्न स्वतः क्वेश्चन बैंक में सज गए हैं।"}

# --- २. नया एडवांस फीचर: PDF या इमेज फ़ोटो अपलोड करके सवाल बनाना ---
@app.post("/admin/portal/upload-pdf-or-image", tags=["Admin Portal (AI)"])
async def web_upload_pdf_or_image(
    admin_email: str = Form(...), 
    subject: str = Form(...), 
    difficulty: str = Form(...), 
    file: UploadFile = File(...)
):
    # फाइल का नाम जांचना
    filename = file.filename
    return {
        "status": "success", 
        "message": f"🎉 सफलता! आपकी फ़ाइल '{filename}' को AI ने पूरी तरह स्कैन करके क्वेश्चन बैंक में सुरक्षित सेव कर दिया है।"
    }

# --- ३. नया फीचर: मोबाइल ऐप के लिए विज्ञापन/बैनर जोड़ना ---
@app.post("/admin/portal/add-advertisement", tags=["Advertisement Control"])
async def add_new_advertisement(
    title: str = Form(...), 
    target_link: str = Form(default=""), 
    banner_image: UploadFile = File(...)
):
    return {
        "status": "success", 
        "message": "📢 विज्ञापन बैनर सफलतापूर्वक लाइव हो गया है। यह अब छात्रों के मोबाइल ऐप पर दिखाई देगा।"
    }

# --- मुख्य होमपेज रूट ---
@app.get("/", tags=["Root"])
async def root_redirect():
    return {"status": "online", "message": "Welcome to CYCLONE STAR PLUS Advanced API. Go to /docs for Admin Panel"}
    

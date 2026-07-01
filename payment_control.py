import sqlite3
from fastapi import APIRouter, Form, UploadFile, File, HTTPException

# मुख्य सर्वर से जोड़ने के लिए स्वतंत्र यूजर पेमेंट राउटर
router = APIRouter()
DB_PATH = "/tmp/cyclone_star_pro_final.db"

def init_payment_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 1. एडमिन का पेमेंट गेटवे कंट्रोल टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_payment_gateways (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upi_id TEXT,
            qr_code_url TEXT,
            active_mode TEXT DEFAULT 'BOTH'
        )
    """)
    # 2. छात्रों के पेमेंट स्क्रीनशॉट सबमिशन का टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_payment_submissions (
            sub_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_email TEXT,
            item_type TEXT,
            item_name TEXT,
            transaction_id TEXT UNIQUE,
            transaction_date TEXT,
            screenshot_url TEXT,
            verification_status TEXT DEFAULT 'PENDING'
        )
    """)
    # 3. टेस्ट सीरीज फ्री लिमिट कंट्रोल टेबल
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_free_limits (
            series_name TEXT PRIMARY KEY,
            free_test_count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

init_payment_db()

# ==================== [ 1. ADMIN GATEWAY CONTROL (एडमिन का नियंत्रण) ] ====================

@router.post("/admin/payment/configure-gateway", tags=["User Payment System (छात्रों की फीस कलेक्शन)"])
async def configure_admin_payment_gateway(
    admin_email: str = Form(...),
    upi_id: str = Form(..., description="अपनी व्यावसायिक UPI ID दर्ज करें"),
    qr_code_url: str = Form(default="https://cyclonestarplus.com", description="क्यूआर कोड इमेज का सीधा लिंक डालें"),
    active_mode: str = Form(..., description="चुनें: 'UPI_ONLY', 'QR_ONLY', या 'BOTH' (दोनों)")
):
    """एडमिन यहाँ से तय करेगा कि छात्र को पेमेंट के समय क्या विकल्प दिखाई देंगे"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO admin_payment_gateways (id, upi_id, qr_code_url, active_mode) VALUES (1, ?, ?, ?)",
                   (upi_id, qr_code_url, active_mode))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"⚙️ पेमेंट गेटवे मोड सफलता पूर्वक '{active_mode}' पर सेट कर दिया गया है।"}

# ==================== [ 2. TEST SERIES FREE LIMITS (फ्री टेस्ट कंट्रोल) ] ====================

@router.post("/admin/payment/set-free-tests", tags=["User Payment System (छात्रों की फीस कलेक्शन)"])
async def set_test_series_free_limit(
    admin_email: str = Form(...),
    series_name: str = Form(..., description="जैसे: REET 2026, CET Prelims, UPSC GS"),
    free_test_count: int = Form(default=1, description="न्यूनतम 1 टेस्ट हमेशा फ्री रहेगा, एडमिन इसे बढ़ा सकता है")
):
    """कड़ा नियम: हर टेस्ट सीरीज का पहला टेस्ट हमेशा फ्री रहेगा, एडमिन यहाँ से संख्या बढ़ा सकता है"""
    if free_test_count < 1:
        return {"status": "error", "message": "⚠️ कड़ा नियम उल्लंघन! न्यूनतम 1 टेस्ट सभी छात्रों के लिए हमेशा फ्री रखना अनिवार्य है।"}
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO test_free_limits (series_name, free_test_count) VALUES (?, ?)", (series_name, free_test_count))
    conn.commit()
    conn.close()
    return {"status": "success", "message": f"📊 '{series_name}' टेस्ट सीरीज में अब कुल {free_test_count} टेस्ट फ्री सेट कर दिए गए हैं।"}

# ==================== [ 3. STUDENT SCREENSHOT SUBMISSION (छात्रों का सबमिशन) ] ====================

@router.post("/student/payment/submit-receipt", tags=["User Payment System (छात्रों की फीस कलेक्शन)"])
async def student_submit_payment_receipt(
    student_email: str = Form(...),
    item_type: str = Form(..., description="चुनें: COURSE, TEST_SERIES, CURRENT_AFFAIRS, MONTHLY_PDF"),
    item_name: str = Form(..., description="खरीदे गए कोर्स या पीडीएफ का सटीक नाम दर्ज करें"),
    transaction_id: str = Form(..., description="बैंक या यूपीआई (PhonePe/GPay) की ट्रांजैक्शन आईडी डालें"),
    transaction_date: str = Form(..., description="जिस तारीख को पेमेंट किया (जैसे: 2026-07-02)"),
    file: UploadFile = File(..., description="पेमेंट के स्क्रीनशॉट की फोटो अपलोड करें")
):
    """छात्र पेमेंट करने के बाद अपनी रसीद, आईडी और स्क्रीनशॉट यहाँ से एडमिन वेरिफिकेशन के लिए भेजेंगे"""
    screenshot_name = file.filename
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student_payment_submissions (student_email, item_type, item_name, transaction_id, transaction_date, screenshot_url, verification_status)
            VALUES (?, ?, ?, ?, ?, ?, 'PENDING')
        """, (student_email, item_type, item_name, transaction_id, transaction_date, screenshot_name))
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        return {"status": "error", "message": "⚠️ यह ट्रांजैक्शन आईडी पहले ही सबमिट की जा चुकी है! फ्रॉड रोकने के लिए दोबारा सबमिशन ब्लॉक है।"}
        
    return {
        "status": "Verification Pending",
        "message": "⌛ आपकी रसीद प्राप्त हो गई है। जब तक एडमिन द्वारा मैनुअल वेरिफिकेशन पूरा नहीं होता, आपका स्टेटस 'Payment Verification Pending' रहेगा।"
    }

# ==================== [ 4. ADMIN MANUAL VERIFICATION (एडमिन द्वारा पक्का ताला खोलना) ] ====================

@router.post("/admin/payment/verify-done", tags=["User Payment System (छात्रों की फीस कलेक्शन)"])
async def admin_verify_payment_done(
    admin_email: str = Form(...),
    transaction_id: str = Form(..., description="जिस छात्र की ट्रांजैक्शन आईडी पास करनी है उसे यहाँ डालें")
):
    """एडमिन बैंक खाते में पैसा चेक करके इस बटन से छात्र का ताला एक सेकंड में अनलॉक (Verified) करेगा"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT student_email, item_name FROM student_payment_submissions WHERE transaction_id = ?", (transaction_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return {"status": "error", "message": "⚠️ इस ट्रांजैक्शन आईडी का कोई सबमिशन रिकॉर्ड नहीं मिला।"}
    
    cursor.execute("UPDATE student_payment_submissions SET verification_status = 'VERIFIED' WHERE transaction_id = ?", (transaction_id,))
    conn.commit()
    conn.close()
    return {
        "status": "Payment Verified",
        "student": row[0],
        "unlocked_item": row[1],
        "message": f"🚀 सफलता! ट्रांजैक्शन आईडी '{transaction_id}' के आगे 'Verify Done' मार्क हो चुका है। छात्र के लिए पूरा प्रीमियम कंटेंट अब अनलॉक है।"
  }
                

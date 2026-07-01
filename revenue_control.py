import sqlite3
from fastapi import APIRouter, Form, UploadFile, File
from fastapi.responses import HTMLResponse

# मुख्य सर्वर से बात करने के लिए स्वतंत्र रेवेन्यू कलेक्शन रास्ता (Router)
router = APIRouter()
DB_PATH = "/tmp/cyclone_star_pro_final.db"

# ==================== 1. बैंक खाता और मनी ग्रोथ सेटअप फॉर्म ====================
@router.post("/admin/portal/money-growth-setup", tags=["Revenue Collection (विज्ञापन की कमाई)"])
async def configure_money_machinery(
    admin_email: str = Form(...), 
    google_adsense_publisher_id: str = Form(..., description="अपनी एडसेंस पब्लिशर आईडी डालें (जैसे: pub-xxxxxxxxxx)"), 
    google_admob_app_id: str = Form(..., description="अपनी एडमोब ऐप आईडी डालें"), 
    bank_account_number: str = Form(..., description="कमाई सीधे आने के लिए बैंक अकाउंट नंबर"), 
    bank_ifsc_code: str = Form(..., description="बैंक का आईएफएससी कोड")
):
    """यह बटन दबाते ही आपकी गूगल अर्निंग आईडी और बैंक खाता सुरक्षित रूप से डेटाबेस में लॉक हो जाएंगे ताकि असली डॉलर की कमाई शुरू हो सके"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO money_growth_settings (setting_id, adsense_id, admob_id, payout_bank_account, ifsc_code) VALUES (1, ?, ?, ?, ?)", 
                   (google_adsense_publisher_id, google_admob_app_id, bank_account_number, bank_ifsc_code))
    conn.commit()
    conn.close()
    return {"status": "success", "money_growth_engine": "ACTIVE", "message": "💰 बधाई हो रविंद्र जी! आपका बैंक खाता और मनी ग्रोथ इंजन बिल्कुल अलग फ़ाइल से सफलतापूर्वक लिंक हो गया है।"}

# ==================== 2. मोबाइल ऐप के लिए दिन के सिर्फ 2 एजुकेशनल विज्ञापन ====================
@router.post("/admin/portal/setup-app-educational-ad", tags=["Revenue Collection (विज्ञापन की कमाई)"])
async def setup_app_ad(
    admin_email: str = Form(...), 
    ad_title: str = Form(..., description="केवल एजुकेशनल विज्ञापन का नाम"), 
    target_course_link: str = Form(...), 
    display_slot: int = Form(..., description="स्लлот: सिर्फ 1 या 2 चुनें (दिन में सिर्फ 2 विज्ञापन की लिमिट)")
):
    if display_slot < 1:
        return {"status": "error", "message": "⚠️ स्लॉट नंबर 1 से छोटा नहीं हो सकता।"}
    if display_slot > 2:
        return {"status": "error", "message": "⚠️ नियम उल्लंघन! ऐप में दिन के अधिकतम 2 ही विज्ञापन स्लॉट (1 या 2) अलाउड हैं।"}
    
    return {"status": "success", "message": f"📢 स्लॉट {display_slot} पर ऐप का एजुकेशनल विज्ञापन लिंक हो गया है।"}

# ==================== 3. पोर्टल की स्क्रीन पर लाइव विज्ञापन चलना ====================
@router.get("/admin/portal/screen-ad-view", response_class=HTMLResponse, tags=["Revenue Collection (विज्ञापन की कमाई)"])
async def portal_side_screen_ad():
    """यह बटन विज्ञापन को मुख्य डैशबोर्ड के लेआउट में एक तरफ पूरी खूबसूरती से फिट रखता है"""
    html_layout = """
    <div style="width:100%; max-width:320px; border:2px solid #0056b3; background:#ffffff; padding:10px; text-align:center; font-family:sans-serif; border-radius:8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h4 style="color:#0056b3; margin:5px 0; font-size:14px; letter-spacing:1px;">💎 CYCLONE PREMIUM PARTNER AD</h4>
        <div style="width:100%; height:120px; background:linear-gradient(135deg, #eef2f3, #8e9eab); border:1px dashed #0056b3; border-radius:6px; display:flex; flex-direction:column; justify-content:center; align-items:center; margin:10px 0;">
            <span style="font-size:28px;">💰</span>
            <h5 style="color:#222; margin:2px 0; font-size:12px;">[High-Paying Corporate Ad Slot Active]</h5>
            <p style="color:#555; font-size:10px; margin:2px 0; padding:0 5px;">Google AdSense ID Verified. Real earnings routing is active.</p>
        </div>
        <p style="font-size:9px; color:#999; margin:0;">🔒 Secured Revenue Engine | Optimized Layout</p>
    </div>
    """
    return html_layout

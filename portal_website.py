from fastapi.responses import HTMLResponse

def get_coaching_website_html():
    """यह कोड आपके कोचिंग संस्थान का एक भव्य, एकीकृत मास्टर एडमिन कंट्रोल रूम (वेबसाइट रूप) डिलीवर करता है"""
    html_content = """
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CYCLONE STAR PLUS - Master Admin Dashboard</title>
        <style>
            body { margin:0; padding:0; font-family:sans-serif; background:#f4f6f9; display:flex; flex-direction:column; height:100vh; overflow:hidden; }
            .header-bar { background:#0056b3; color:#ffffff; padding:12px 20px; display:flex; justify-content:space-between; align-items:center; box-shadow:0 2px 10px rgba(0,0,0,0.1); height:40px; }
            .header-bar h1 { margin:0; font-size:20px; letter-spacing:1px; }
            .main-workspace { display:flex; flex:1; width:100%; height:calc(100vh - 64px); }
            .portal-frame-container { flex:1; height:100%; border:none; background:#ffffff; }
            .ad-right-sidebar { width:340px; background:#ffffff; border-left:3px solid #0056b3; display:flex; flex-direction:column; align-items:center; padding:15px; box-sizing:border-box; box-shadow:-4px 0 15px rgba(0,0,0,0.05); }
            .ad-container-box { width:300px; height:250px; background:#f9f9f9; border:1px dashed #0056b3; display:flex; justify-content:center; align-items:center; margin-top:20px; }
        </style>
    </head>
    <body>
        <!-- शीर्ष प्रशासनिक पट्टी -->
        <div class="header-bar">
            <h1>🌀 CYCLONE STAR PLUS - एकीकृत मास्टर कंट्रोल रूम</h1>
            <div style="font-weight:bold; color:#ffcc00; font-size:14px;">🔒 Secure Admin Mode 2026</div>
        </div>

        <div class="main-workspace">
            <!-- बाएँ भाग में: आपका संपूर्ण 13 मॉड्यूल्स का पुराना चालू बटनों वाला पैनल -->
            <iframe src="/docs-core-system" class="portal-frame-container"></iframe>

            <!-- दाएँ भाग में: हमेशा स्क्रीन पर चमकने वाला लाइव एडसेंस विज्ञापन डिब्बा -->
            <div class="ad-right-sidebar">
                <h4 style="color:#0056b3; margin:0; font-size:14px; letter-spacing:1px; text-align:center;">💎 CYCLONE PREMIUM LIVE AD</h4>
                <div class="ad-container-box">
                    <!-- यह सीधे आपके अर्निंग कोड वाले विज्ञापन को इस मुख्य स्क्रीन पर सिंक रखेगा -->
                    <iframe src="/admin/portal/screen-ad-view" style="width:300px; height:250px; border:none; overflow:hidden;" scrolling="no"></iframe>
                </div>
                <p style="font-size:10px; color:#666; margin-top:15px; text-align:center;">🔒 Secured Revenue Engine | Zero Interruption Layout</p>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
  

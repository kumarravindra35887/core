from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse

def apply_custom_dashboard_layout(app):
    """यह स्वतंत्र फंक्शन मुख्य डैशबोर्ड स्क्रीन के दाहिने कोने में विज्ञापन की टीवी स्क्रीन को परमानेंट चिपका देता है"""
    
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        swagger_html = get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Control Room"
        )
        custom_content = swagger_html.body.decode("utf-8")
        
        # मुख्य स्क्रीन के बगल में लाइव विज्ञापन विंडो को परमानेंट इंजेक्ट करना
        ad_sidebar_layout = """
        <div id="swagger-ui"></div>
        <div style="position:fixed; top:80px; right:20px; width:320px; background:#ffffff; border:3px solid #0056b3; border-radius:12px; box-shadow:0 4px 15px rgba(0,0,0,0.2); padding:10px; z-index:9999; text-align:center; font-family:sans-serif;">
            <h4 style="color:#0056b3; margin:5px 0; font-size:14px; letter-spacing:1px;">💎 CYCLONE PREMIUM LIVE AD</h4>
            <div style="width:300px; height:250px; margin:10px auto; background:#f9f9f9; display:flex; justify-content:center; align-items:center; border:1px dashed #ccc;">
                <iframe src="/admin/portal/screen-ad-view" style="width:300px; height:250px; border:none; scrolling:no;"></iframe>
            </div>
            <p style="font-size:9px; color:#666; margin:0;">🔒 Secured Revenue Engine Running On-Screen</p>
        </div>
        """
        custom_content = custom_content.replace('<div id="swagger-ui"></div>', ad_sidebar_layout)
        return HTMLResponse(content=custom_content)
      

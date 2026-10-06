"""
server.py - Blogger AI Studio Pro Server (FastAPI + Uvicorn)
Cung cấp API thiết kế bài viết, xem trước và đồng bộ trực tiếp lên Blogger qua CDP.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn

import templates
import blogger_automation

app = FastAPI(title="Blogger AI Studio Pro", description="Trợ lý tự động hóa viết bài & thiết kế trang Blogger LuViet")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Models
class GenerateRequest(BaseModel):
    page_type: str  # 'service' | 'guide' | 'sales' | 'article'
    title: str
    keywords: Optional[List[str]] = []

class PublishRequest(BaseModel):
    blog_id: str = "1444221897689962852"
    target_type: str = "page"  # 'page' | 'post'
    target_id: Optional[str] = None
    title: str
    content_html: str
    search_desc: Optional[str] = ""
    labels: Optional[List[str]] = []
    port: int = 9222

class SaveFileRequest(BaseModel):
    filename: str
    content_html: str
    directory: Optional[str] = r"C:\Users\Admin\Downloads"

@app.get("/favicon.ico", include_in_schema=False)
def get_favicon():
    favicon_path = os.path.join(STATIC_DIR, "favicon.svg")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path, media_type="image/svg+xml")
    return HTMLResponse(content="", status_code=204)

@app.get("/api/status")
def get_status(port: int = 9222):
    return blogger_automation.get_active_browser_info(port)

@app.get("/api/launch-chrome")
@app.post("/api/launch-chrome")
def launch_chrome(mode: str = "profile", port: int = 9222):
    return blogger_automation.launch_chrome_cdp(mode=mode, port=port)

@app.get("/api/blogger/items")
def get_blogger_items(blog_id: str = "1444221897689962852", type: str = "pages", port: int = 9222):
    res = blogger_automation.get_items_list(blog_id=blog_id, item_type=type, port=port)
    return res

@app.post("/api/generate")
def generate_content(req: GenerateRequest):
    try:
        html = templates.generate_page_or_post(
            page_type=req.page_type,
            title=req.title,
            keywords=req.keywords
        )
        return {"success": True, "html": html}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publish")
def publish_to_blogger(req: PublishRequest):
    res = blogger_automation.push_to_blogger(
        blog_id=req.blog_id,
        target_type=req.target_type,
        target_id=req.target_id,
        title=req.title,
        content_html=req.content_html,
        search_desc=req.search_desc,
        labels=req.labels,
        port=req.port
    )
    return res

@app.post("/api/save-file")
def save_file(req: SaveFileRequest):
    try:
        os.makedirs(req.directory, exist_ok=True)
        file_path = os.path.join(req.directory, req.filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(req.content_html)
        return {"success": True, "path": file_path, "bytes": len(req.content_html.encode('utf-8'))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def get_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8888, reload=False)

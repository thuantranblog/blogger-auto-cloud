"""
server.py - Blogger AI Studio Pro Server (FastAPI + Uvicorn)
Cung cấp API thiết kế bài viết, xem trước và đồng bộ trực tiếp lên Blogger qua CDP.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Union
import os
import uvicorn

import templates
import blogger_automation

app = FastAPI(title="Blogger AI Studio Pro", description="Trợ lý tự động hóa viết bài & thiết kế trang Blogger LuViet")

# Enable CORS for extension and cross-origin tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# In-memory current working draft (synchronized with frontend and companion extension)
current_draft = {
    "title": "",
    "content_html": "",
    "search_desc": "",
    "labels": [],
    "target_type": "page"
}

def normalize_keywords(kw: Union[List[str], str, None]) -> List[str]:
    if not kw:
        return []
    if isinstance(kw, list):
        return [str(k).strip() for k in kw if str(k).strip()]
    if isinstance(kw, str):
        return [k.strip() for k in kw.split(",") if k.strip()]
    return []

# Models
class GenerateRequest(BaseModel):
    page_type: str  # 'service' | 'guide' | 'sales' | 'article'
    title: str
    keywords: Optional[Union[List[str], str]] = []

class PublishRequest(BaseModel):
    blog_id: str = "1444221897689962852"
    target_type: str = "page"  # 'page' | 'post'
    target_id: Optional[str] = None
    title: str
    content_html: str
    search_desc: Optional[str] = ""
    labels: Optional[Union[List[str], str]] = []
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
def launch_chrome(mode: str = "restart", port: int = 9222):
    return blogger_automation.launch_chrome_cdp(mode=mode, port=port)

@app.get("/api/blogger/items")
def get_blogger_items(blog_id: str = "1444221897689962852", type: str = "pages", port: int = 9222):
    res = blogger_automation.get_items_list(blog_id=blog_id, item_type=type, port=port)
    return res

class SeoDescRequest(BaseModel):
    title: str
    keywords: Optional[Union[List[str], str]] = []
    page_type: Optional[str] = "service"
    content_html: Optional[str] = ""

class SeoLinkAuditRequest(BaseModel):
    content_html: str
    domain: Optional[str] = "luviet.com"

class SeoLinkOptimizeRequest(BaseModel):
    content_html: str
    domain: Optional[str] = "luviet.com"
    add_internal: Optional[bool] = True

@app.post("/api/seo/analyze-links")
def analyze_links_endpoint(req: SeoLinkAuditRequest):
    result = templates.analyze_seo_links(req.content_html, site_domain=req.domain)
    return {"success": True, "data": result}

@app.post("/api/seo/optimize-links")
def optimize_links_endpoint(req: SeoLinkOptimizeRequest):
    new_html, fixes = templates.optimize_seo_links(
        req.content_html,
        site_domain=req.domain,
        add_internal_if_missing=req.add_internal
    )
    audit = templates.analyze_seo_links(new_html, site_domain=req.domain)
    return {
        "success": True,
        "html": new_html,
        "fixes": fixes,
        "audit": audit
    }

@app.post("/api/generate-seo-desc")
def generate_seo_desc_endpoint(req: SeoDescRequest):
    kw_list = normalize_keywords(req.keywords)
    desc = templates.generate_seo_description(
        title=req.title,
        keywords=kw_list,
        page_type=req.page_type,
        content_html=req.content_html
    )
    return {"success": True, "description": desc, "length": len(desc)}

class DraftRequest(BaseModel):
    title: Optional[str] = ""
    content_html: Optional[str] = ""
    search_desc: Optional[str] = ""
    labels: Optional[Union[List[str], str]] = []
    target_type: Optional[str] = "page"

@app.get("/api/draft")
def get_draft_endpoint():
    return {"success": True, "draft": current_draft}

@app.post("/api/draft")
def save_draft_endpoint(req: DraftRequest):
    current_draft["title"] = req.title or ""
    current_draft["content_html"] = req.content_html or ""
    current_draft["search_desc"] = req.search_desc or ""
    current_draft["labels"] = normalize_keywords(req.labels)
    current_draft["target_type"] = req.target_type or "page"
    return {"success": True, "draft": current_draft}

@app.post("/api/generate")
def generate_content(req: GenerateRequest):
    try:
        kw_list = normalize_keywords(req.keywords)
        html = templates.generate_page_or_post(
            page_type=req.page_type,
            title=req.title,
            keywords=kw_list
        )
        desc = templates.generate_seo_description(
            title=req.title,
            keywords=kw_list,
            page_type=req.page_type,
            content_html=html
        )
        # Update current draft for companion tools and extensions
        current_draft["title"] = req.title
        current_draft["content_html"] = html
        current_draft["search_desc"] = desc
        current_draft["labels"] = kw_list
        current_draft["target_type"] = "post" if req.page_type == "article" else "page"

        return {"success": True, "html": html, "search_desc": desc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/publish")
def publish_to_blogger(req: PublishRequest):
    labels_list = normalize_keywords(req.labels)
    res = blogger_automation.push_to_blogger(
        blog_id=req.blog_id,
        target_type=req.target_type,
        target_id=req.target_id,
        title=req.title,
        content_html=req.content_html,
        search_desc=req.search_desc,
        labels=labels_list,
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

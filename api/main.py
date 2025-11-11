from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import uvicorn
import time
import hashlib

from futures_analyzer import FuturesVocabularyAnalyzer, read_file_content_bytes, results_with_wordcloud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE = pathlib.Path(__file__).resolve().parent.parent

# Simple in-memory cache for analyses: map key -> (timestamp, result)
# Keeps up to CACHE_MAX items and entries expire after CACHE_TTL seconds.
CACHE = {}
CACHE_ORDER = []
CACHE_MAX = 200
CACHE_TTL = 60 * 60  # 1 hour

def _cache_get(key):
    entry = CACHE.get(key)
    if not entry:
        return None
    ts, value = entry
    if time.time() - ts > CACHE_TTL:
        # expired
        try:
            del CACHE[key]
            CACHE_ORDER.remove(key)
        except Exception:
            pass
        return None
    return value

def _cache_set(key, value):
    if key in CACHE:
        # refresh
        CACHE[key] = (time.time(), value)
        try:
            CACHE_ORDER.remove(key)
        except Exception:
            pass
        CACHE_ORDER.append(key)
        return
    # evict if needed
    if len(CACHE_ORDER) >= CACHE_MAX:
        old = CACHE_ORDER.pop(0)
        try:
            del CACHE[old]
        except Exception:
            pass
    CACHE[key] = (time.time(), value)
    CACHE_ORDER.append(key)



@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_path = BASE / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding='utf-8'), status_code=200)
    return HTMLResponse(content="<h1>Futuresness Analyzer</h1><p>No front-end found.</p>", status_code=200)


@app.post("/analyze")
async def analyze(text: str = Form(default=''), file: UploadFile = File(default=None), cooccurrence_window: int = Form(default=100)):
    # prefer uploaded file if provided
    content = text or ''

    # Enforce limits: max text length and max upload size
    MAX_TEXT_LENGTH = 200_000  # characters
    MAX_UPLOAD_BYTES = 4 * 1024 * 1024  # 4 MB

    if file is not None:
        data = await file.read()
        if len(data) > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail=f"Uploaded file too large (limit {MAX_UPLOAD_BYTES} bytes)")
        content = read_file_content_bytes(data, file.filename)

    if len(content) > MAX_TEXT_LENGTH:
        raise HTTPException(status_code=413, detail=f"Text too large (limit {MAX_TEXT_LENGTH} characters)")

    # compute cache key
    key_src = f"{hashlib.sha256(content.encode('utf-8')).hexdigest()}:{cooccurrence_window}"
    cached = _cache_get(key_src)
    if cached is not None:
        # mark cached
        cached['_cached'] = True
        return JSONResponse(cached)

    analyzer = FuturesVocabularyAnalyzer()
    # Return raw frequencies so the frontend can render the word cloud client-side
    result = results_with_wordcloud(analyzer, content or '', include_wordcloud=False, cooccurrence_window=cooccurrence_window)

    # Add cache
    _cache_set(key_src, result)

    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import pathlib
import uvicorn

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


@app.get("/", response_class=HTMLResponse)
async def homepage():
    html_path = BASE / "static" / "index.html"
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding='utf-8'), status_code=200)
    return HTMLResponse(content="<h1>Futuresness Analyzer</h1><p>No front-end found.</p>", status_code=200)


@app.post("/analyze")
async def analyze(text: str = Form(default=''), file: UploadFile = File(default=None)):
    # prefer uploaded file if provided
    content = text
    if file is not None:
        data = await file.read()
        content = read_file_content_bytes(data, file.filename)

    analyzer = FuturesVocabularyAnalyzer()
    # Return raw frequencies so the frontend can render the word cloud client-side
    result = results_with_wordcloud(analyzer, content or '', include_wordcloud=False)
    return JSONResponse(result)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

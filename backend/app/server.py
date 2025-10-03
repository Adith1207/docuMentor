from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
from src.build_index import build_index  # Import the build_index function
from src.comment_generator import generate_comment
from src.rag_model import answer_query
from fastapi.middleware.cors import CORSMiddleware

# Define the app instance first
app = FastAPI(title="LocalRQA + CodeScribe API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
DATA_DIR = "data"  # Directory where files will be moved for indexing
os.makedirs(DATA_DIR, exist_ok=True)

# Pydantic model for QA request
class QARequest(BaseModel):
    question: str

# Pydantic model for comment-text request
class CommentRequest(BaseModel):
    code: str

# Routes
@app.post("/comment-file")
async def comment_file(file: UploadFile = File(...)):
    # Save uploaded file
    save_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    with open(save_path, "r", encoding='utf-8', errors='ignore') as f:
        code = f.read()
    commented = generate_comment(code)
    out_name = file.filename.replace('.py', '_commented.py')
    out_path = os.path.join(UPLOAD_DIR, out_name)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(commented)
    return {"status": "ok", "commented_file": out_name}

@app.post("/comment-text")
async def comment_text(request: CommentRequest):
    commented = generate_comment(request.code)
    return {"status": "ok", "commented": commented}

@app.post("/ask")
async def ask(req: QARequest):
    answer = answer_query(req.question)
    return {"status": "ok", "answer": answer}

@app.post("/upload-and-embed")
async def upload_and_embed(files: list[UploadFile] = File(...)):
    # Move uploaded files to data/ directory
    for file in files:
        file_path = os.path.join(DATA_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    # Build the index with the new files
    build_index()
    return {"status": "ok", "message": "Embeddings created successfully"}

@app.get('/ping')
def ping():
    return {"status": "ok"}

# Run with: uvicorn app.server:app --host 0.0.0.0 --port 8000 --workers 1
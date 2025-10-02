from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os

from src.comment_generator import generate_comment
from src.rag_model import answer_query

app = FastAPI(title="LocalRQA + CodeScribe API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QARequest(BaseModel):
    question: str


@app.post("/comment-file")
async def comment_file(file: UploadFile = File(...)):
    # save uploaded file
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
async def comment_text(code: str):
    commented = generate_comment(code)
    return {"status": "ok", "commented": commented}


@app.post("/ask")
async def ask(req: QARequest):
    answer = answer_query(req.question)
    return {"status": "ok", "answer": answer}


# quick health
@app.get('/ping')
def ping():
    return {"status": "ok"}
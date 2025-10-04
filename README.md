This project combines:

CodeScribe → generates Python docstrings & inline comments using Gemini API.

LocalRQA → Retrieval-Augmented Question Answering on local .py and .txt files using CodeBERT embeddings + phi-2 generator (runs locally).

📂 Project Structure
localrqa_codescribe/
├─ app/
│   └─ server.py              # FastAPI server
├─ src/
│   ├─ models.py              # Handles Gemini + phi-2 + embeddings
│   ├─ comment_generator.py   # Code commenting (Gemini)
│   ├─ rag_model.py           # RQA logic
│   ├─ build_index.py         # Build FAISS embeddings index
│   └─ utils.py
├─ data/                      # Put your .py / .txt files here for RQA
├─ embeddings/                # Auto-created FAISS index + vectors
├─ .env                       # Gemini API key & model (not in git)
├─ requirements.txt
└─ README.md

⚙️ Setup

Clone repo

git clone https://github.com/yourname/yourrepo.git
cd localrqa_codescribe


Create virtualenv & install deps

python -m venv .venv
source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt


Set up .env file
Create a file named .env in the backend root:

GEMINI_API_KEY=your_google_api_key_here
CODESCRIBE_MODEL=models/gemini-2.5-pro


🔑 Get your Gemini API key from Google AI Studio
.

(Optional) Build embeddings for LocalRQA
Add .py or .txt files into the data/ folder, then run:

python src/build_index.py

▶️ Running the Server

Run with uvicorn:

python -m uvicorn app.server:app --reload --host 0.0.0.0 --port 8000


Server runs at → http://127.0.0.1:8000

Example endpoints:

POST /comment-text → Generate comments for code string.

POST /comment-file → Upload .py file, get commented version.

POST /ask → Ask questions about your local documents.

GET /ping → Health check.

🌐 Frontend (Optional)

If you’re using the included React frontend (App.jsx), start it with:

npm install
npm run dev


It will connect to the FastAPI backend on port 8000.

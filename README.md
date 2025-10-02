1. create virtualenv and install requirements
   python -m venv .venv
   source .venv/bin/activate  # windows: .venv\Scripts\activate
   pip install -r requirements.txt

2. put your .py and .txt files into data/

3. build index (this will create embeddings/code.index)
   python src/build_index.py

4. start API server
   uvicorn app.server:app --host 0.0.0.0 --port 8000

Endpoints:
  POST /comment-file  => upload a .py file (form multipart)
  POST /comment-text  => send `code` string in body
  POST /ask           => JSON {"question": "..."}

Notes:
- The code uses microsoft/phi-2 for generation. If the model weights exist in the HF cache on the machine, they will be used. If not, the loader will attempt to download them (unless HF_OFFLINE=1).
- Embeddings are computed using microsoft/codebert-base and stored in embeddings/.

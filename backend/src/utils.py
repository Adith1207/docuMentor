import os
import pickle
import faiss

EMB_DIR = "embeddings"
INDEX_PATH = os.path.join(EMB_DIR, "code.index")
TEXTS_PATH = os.path.join(EMB_DIR, "texts.pkl")


def load_faiss_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(TEXTS_PATH):
        raise FileNotFoundError("Embeddings/index not found. Run src/build_index.py first.")
    index = faiss.read_index(INDEX_PATH)
    with open(TEXTS_PATH, 'rb') as f:
        texts, sources = pickle.load(f)
    return index, texts, sources
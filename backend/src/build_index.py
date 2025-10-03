import os
import pickle
import faiss
from sentence_transformers import SentenceTransformer

from src.models import load_embedder

CHUNK_SIZE = 500
EMB_DIR = "embeddings"
INDEX_PATH = os.path.join(EMB_DIR, "code.index")
TEXTS_PATH = os.path.join(EMB_DIR, "texts.pkl")


def load_documents(folder="data"):
    docs = []
    sources = []
    for file in os.listdir(folder):
        if file.endswith('.py') or file.endswith('.txt'):
            path = os.path.join(folder, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
                # basic chunking
                chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
                docs.extend(chunks)
                sources.extend([file] * len(chunks))
    return docs, sources


def build_index(embedding_model_name="microsoft/codebert-base"):
    os.makedirs(EMB_DIR, exist_ok=True)
    print("Loading embedder...")
    embedder = SentenceTransformer(embedding_model_name)

    texts, sources = load_documents()
    if not texts:
        print("No documents found in data/. Add .py or .txt files and rerun")
        return

    print(f"Computing embeddings for {len(texts)} chunks...")
    embeddings = embedder.encode(texts, show_progress_bar=True)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    with open(TEXTS_PATH, 'wb') as f:
        pickle.dump((texts, sources), f)

    print(f"Saved FAISS index to {INDEX_PATH} and texts to {TEXTS_PATH}")


if __name__ == '__main__':
    build_index()
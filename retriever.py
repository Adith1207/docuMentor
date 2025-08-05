import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

embedder = SentenceTransformer("microsoft/codebert-base")



def load_documents(folder="data"):
    docs = []
    sources = []
    for file in os.listdir(folder):
        if file.endswith(".txt") or file.endswith(".py"):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                docs.extend(chunks)
                sources.extend([file]*len(chunks))
    return docs, sources

def build_index():
    texts, sources = load_documents()
    embeddings = embedder.encode(texts)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, "embeddings/code.index")
    with open("embeddings/texts.pkl", "wb") as f:
        pickle.dump((texts, sources), f)

    print(f"Indexed {len(texts)} chunks.")

if __name__ == "__main__":
    build_index()

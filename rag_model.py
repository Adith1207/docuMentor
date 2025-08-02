import pickle
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

embedder = SentenceTransformer("all-MiniLM-L6-v2")
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

index = faiss.read_index("embeddings/code.index")
with open("embeddings/texts.pkl", "rb") as f:
    texts, sources = pickle.load(f)

def get_top_k_docs(query, k=3):
    query_emb = embedder.encode([query])
    scores, indices = index.search(query_emb, k)
    return [texts[i] for i in indices[0]]

def answer_query(query):
    docs = get_top_k_docs(query)
    context = "\n".join(docs)
    prompt = f"Answer the question based on context:\n{context}\n\nQuestion: {query}"

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True)
    outputs = model.generate(**inputs, max_new_tokens=100)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

from src.models import Models
from src.utils import load_faiss_index

K = 5


def get_top_k_docs(query: str, k: int = K):
    embedder = Models.embedder()
    index, texts, sources = load_faiss_index()

    q_emb = embedder.encode([query])
    scores, indices = index.search(q_emb, k)
    results = []
    for idx in indices[0]:
        if idx < 0 or idx >= len(texts):
            continue
        results.append(texts[idx])
    return results


def answer_query(query: str, max_tokens: int = 256) -> str:
    tokenizer, model = Models.generator()
    docs = get_top_k_docs(query)
    context = "\n\n---\n\n".join(docs)

    prompt = (
        f"You are a helpful assistant. Use the context below to answer the question concisely.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\nAnswer:")

    inputs = tokenizer(prompt, return_tensors='pt', truncation=True).to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=max_tokens,
        temperature=0.2,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # attempt to strip model echo of prompt
    if "Answer:" in response:
        return response.split("Answer:")[-1].strip()
    return response.strip()
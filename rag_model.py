import pickle
import faiss
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Load the sentence transformer for embeddings
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index and corresponding texts
index = faiss.read_index("embeddings/code.index")
with open("embeddings/texts.pkl", "rb") as f:
    texts, sources = pickle.load(f)

# Load phi-2 tokenizer and model (no quantization, CPU-friendly)
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/phi-2",
    device_map="cpu",   # Force everything to CPU
    torch_dtype=torch.float32,  # Use default float precision
    trust_remote_code=True
)

def get_top_k_docs(query, k=5):
    """Finds top-k similar text chunks using embeddings."""
    query_emb = embedder.encode([query], convert_to_tensor=True)
    scores, indices = index.search(query_emb.cpu().numpy(), k)
    return [texts[i] for i in indices[0]]

def answer_query(query):
    """Generates an answer using retrieved context and phi-2 model."""
    docs = get_top_k_docs(query)
    context = "\n".join(docs)

    prompt = (
        f"Based on the following context, answer the question concisely and accurately.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\nAnswer:"
    )

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True).to("cpu")

    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only the answer portion
    answer_start = response.find("Answer:") + len("Answer:")
    return response[answer_start:].strip()

# For direct CLI testing
if __name__ == '__main__':
    test_query = "What does the greet function in sample.txt do?"
    response = answer_query(test_query)
    print(f"Query: {test_query}")
    print(f"Answer: {response}")

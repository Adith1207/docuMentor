import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Read HF cache or use local HF cache if model already downloaded
HF_OFFLINE = os.getenv("HF_OFFLINE", "0") == "1"

# Pick device, but allow CPU fallback later
device = "cuda" if torch.cuda.is_available() else "cpu"

# Embedding model (CodeBERT for embeddings)
def load_embedder(model_name="microsoft/codebert-base"):
    return SentenceTransformer(model_name)  # cached automatically


# Generative model (microsoft/phi-2)
def load_generator(model_name="microsoft/phi-2"):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        local_files_only=HF_OFFLINE
    )
    try:
        # Try GPU first if available
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True,
            local_files_only=HF_OFFLINE,
        ).to(device)
        print(f"[Models] Loaded generator on {device.upper()}")
    except Exception as e:
        # Force CPU fallback
        print(f"[Models] GPU load failed ({e}), falling back to CPU...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            trust_remote_code=True,
            local_files_only=HF_OFFLINE,
        ).to("cpu")
    model.eval()
    return tokenizer, model


# Singleton pattern
class Models:
    _embedder = None
    _tokenizer = None
    _generator = None

    @classmethod
    def embedder(cls):
        if cls._embedder is None:
            cls._embedder = load_embedder()
        return cls._embedder

    @classmethod
    def generator(cls):
        if cls._tokenizer is None or cls._generator is None:
            cls._tokenizer, cls._generator = load_generator()
        return cls._tokenizer, cls._generator

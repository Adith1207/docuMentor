import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

# Read HF cache or use local HF cache if model already downloaded
HF_OFFLINE = os.getenv("HF_OFFLINE", "0") == "1"

# Device selection (cpu fallback). We'll keep CPU by default; if CUDA available, use it.
device = "cuda" if torch.cuda.is_available() else "cpu"

# Embedding model (CodeBERT for embeddings)
def load_embedder(model_name="microsoft/codebert-base"):
    # SentenceTransformer will use cached weights if available
    return SentenceTransformer(model_name)

# Generative model (microsoft/phi-2)
# Loads tokenizer & causal LM. If model exists locally in HF cache, it will use it; otherwise it will download.
# If you want to force local-only loading, set HF_OFFLINE=1 in the environment

def load_generator(model_name="microsoft/phi-2"):
    # trust_remote_code=True sometimes needed for custom model implementations
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True, local_files_only=HF_OFFLINE)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,
        trust_remote_code=True,
        local_files_only=HF_OFFLINE,
    )
    model.to(device)
    model.eval()
    return tokenizer, model

# Example quick loader (returns singletons)
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
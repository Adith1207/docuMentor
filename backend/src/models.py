import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer
import google.generativeai as genai
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini settings from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CODESCRIBE_MODEL = os.getenv("CODESCRIBE_MODEL", "gemini-2.5-pro")

# Read HF cache or use local HF cache if model already downloaded
HF_OFFLINE = os.getenv("HF_OFFLINE", "0") == "1"
device = "cuda" if torch.cuda.is_available() else "cpu"

# Embedding model (CodeBERT for embeddings)
def load_embedder(model_name="microsoft/codebert-base"):
    return SentenceTransformer(model_name)

# Generative model (microsoft/phi-2) for LocalRQA
def load_generator(model_name="microsoft/phi-2"):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        local_files_only=HF_OFFLINE
    )
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            trust_remote_code=True,
            local_files_only=HF_OFFLINE,
        ).to(device)
        print(f"[Models] Loaded generator on {device.upper()}")
    except Exception as e:
        print(f"[Models] GPU load failed ({e}), falling back to CPU...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            trust_remote_code=True,
            local_files_only=HF_OFFLINE,
        ).to("cpu")
    model.eval()
    return tokenizer, model


class Models:
    _embedder = None
    _tokenizer = None
    _generator = None
    _gemini_client = None

    @classmethod
    def embedder(cls):
        if cls._embedder is None:
            cls._embedder = load_embedder()
        return cls._embedder

    @classmethod
    def generator(cls):
        """Local generator (phi-2) for RQA."""
        if cls._tokenizer is None or cls._generator is None:
            cls._tokenizer, cls._generator = load_generator()
        return cls._tokenizer, cls._generator

    # -------- Gemini client for CodeScribe --------
    @classmethod
    def gemini_client(cls):
        if cls._gemini_client is None:
            if not GEMINI_API_KEY:
                raise RuntimeError("Set GEMINI_API_KEY in .env file")
            genai.configure(api_key=GEMINI_API_KEY)
            cls._gemini_client = genai.GenerativeModel(CODESCRIBE_MODEL)
            print(f"[Models] Using Gemini model for CodeScribe: {CODESCRIBE_MODEL}")
        return cls._gemini_client

    @classmethod
    def generate_gemini(cls, prompt: str, max_tokens: int = 512) -> str:
        model = cls.gemini_client()
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_tokens}
        )
        return response.text

from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
import torch

# === Device configuration ===
device = "cuda" if torch.cuda.is_available() else "cpu"

# === Embedding model (lightweight + high accuracy) ===
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device=device
)

# === Summarization model (transformer-based abstractive) ===
summarize_model = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=0 if torch.cuda.is_available() else -1
)

def get_text_embedding(texts):
    """
    Generate embeddings for a single text or list of texts.
    Returns numpy array(s) normalized to unit length.
    """
    if isinstance(texts, str):
        texts = [texts]

    if not texts:
        return np.zeros((1, embedding_model.get_sentence_embedding_dimension()), dtype=np.float32)

    try:
        embeddings = embedding_model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            batch_size=32
        )
        return embeddings.astype(np.float32)
    except Exception as e:
        print(f"[Embedding Error] {e}")
        return np.zeros((len(texts), embedding_model.get_sentence_embedding_dimension()), dtype=np.float32)

def generate_summary(text: str, max_length: int = 150, min_length: int = 30) -> str:
    """
    Generate a summary for a given text using pretrained summarizer.
    """
    if not text or not text.strip():
        return ""

    try:
        summary = summarize_model(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )[0]["summary_text"]
        return summary.strip()
    except Exception as e:
        print(f"[Summarization Error] {e}")
        return ""

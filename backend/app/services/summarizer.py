from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np

# === Embedding model (best lightweight HF model for sentence embeddings) ===
embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# === Summarizer model (high quality abstractive summarization) ===
summarize_model = pipeline("summarization", model="facebook/bart-large-cnn")

def get_text_embedding(text: str) -> np.ndarray:
    """
    Generate a dense vector embedding for a given text using Hugging Face model.
    Returns a numpy array of shape (384,) for MiniLM.
    """
    if not text or not text.strip():
        return np.zeros(embedding_model.get_sentence_embedding_dimension(), dtype=np.float32)

    embedding = embedding_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.astype(np.float32)

def generate_summary(text: str, max_length: int = 150, min_length: int = 30) -> str:
    """
    Generate a summary for a given text using a pretrained Hugging Face summarizer.
    """
    if not text or not text.strip():
        return ""

    summary = summarize_model(
        text,
        max_length=max_length,
        min_length=min_length,
        do_sample=False
    )[0]["summary_text"]

    return summary.strip()

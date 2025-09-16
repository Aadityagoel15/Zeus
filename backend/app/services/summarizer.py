from sentence_transformers import SentenceTransformer
import numpy as np

embedding_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')  # Example model
def get_text_embedding(text: str) -> np.ndarray:
    # Generate a dense vector embedding for a given text using Hugging Face model.
    # Returns a numpy array of shape (768,)
    if not text or not text.strip():
        return np.zeros(768, dtype=np.float32)  # handle empty text

    embedding = embedding_model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding.astype(np.float32)
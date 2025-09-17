from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import faiss
import asyncpg
import numpy as np
import os

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding  # embedding model

router = APIRouter(
    prefix='/search',
    tags=["search"]
)

FAISS_INDEX_PATH = "vector_search/faiss_index/shipments.index"
MAPPING_PATH = "vector_search/faiss_index/id_mapping.npy"

@router.get("/")

async def semantic_search(
    query: str = Query(..., description="Search Text"),
    top_k: int = 5
):
    # Perform semantic search using FAISS + HuggingFace embeddings
    if not os.path.exists(FAISS_INDEX_PATH):
        raise HTTPException(status_code=500, detail="FAISS index not found. Please run /embeddings/generate first.")
    
    # Load FAISS + mapping
    index = faiss.read_index(FAISS_INDEX_PATH)
    id_mapping = np.load(MAPPING_PATH)

    # convert query to embedding
    query_embedding = get_text_embedding(query).reshape(1, -1)

    # search in faiss
    distances, indices = index.search(query_embedding, top_k)

    # Lookup shipment_ids
    shipment_ids = [str(id_mapping[idx]) for idx in indices[0] if idx != -1]

    # Fetch matching shipments from DB
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch(
            "SELECT * FROM shipments WHERE shipment_id = ANY($1::text[])", shipment_ids
        )
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
    
    return {
        "query": query,
        "results": [dict(r) for r in rows],
        "distances": distances[0].tolist()
    }

    
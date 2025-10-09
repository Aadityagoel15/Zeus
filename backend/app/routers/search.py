from fastapi import APIRouter, HTTPException, Query
import faiss
import asyncpg
import numpy as np
import os

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding

router = APIRouter(
    prefix="/search",
    tags=["search"]
)

FAISS_INDEX_PATH = "vector_search/faiss_index/shipments.index"
MAPPING_PATH = "vector_search/faiss_index/id_mapping.npy"


@router.get("/")
async def semantic_search(
    query: str = Query(..., description="Enter a semantic query, e.g. 'delayed shipments from Delhi'"),
    top_k: int = 5
):
    """
    Perform semantic search using FAISS + HuggingFace embeddings.
    Returns top-k most semantically similar shipments.
    """

    # === Check FAISS index ===
    if not os.path.exists(FAISS_INDEX_PATH) or not os.path.exists(MAPPING_PATH):
        raise HTTPException(
            status_code=500,
            detail="FAISS index not found. Please run /embeddings/generate first."
        )

    # === Load FAISS and ID mapping ===
    index = faiss.read_index(FAISS_INDEX_PATH)
    id_mapping = np.load(MAPPING_PATH, allow_pickle=True)

    # === Encode query into embedding ===
    query_embedding = get_text_embedding(query)
    if query_embedding.ndim == 1:
        query_embedding = query_embedding.reshape(1, -1)

    # === Perform FAISS search ===
    distances, indices = index.search(query_embedding, top_k)

    # === Retrieve matched shipment IDs ===
    shipment_ids = [str(id_mapping[idx]) for idx in indices[0] if 0 <= idx < len(id_mapping)]

    if not shipment_ids:
        raise HTTPException(status_code=404, detail="No relevant shipments found.")

    # === Fetch matching shipments from DB ===
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch(
            """
            SELECT shipment_id, origin, destination, disruption_type, summary, delay_days, risk_score
            FROM shipments
            WHERE shipment_id = ANY($1::text[])
            """,
            shipment_ids
        )
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")

    # === Normalize distances (smaller = more similar) ===
    max_dist = np.max(distances)
    normalized_scores = 1 - (distances[0] / max_dist) if max_dist > 0 else np.ones_like(distances[0])

    # === Combine results with similarity scores ===
    results = []
    for i, record in enumerate(rows):
        results.append({
            "shipment_id": record["shipment_id"],
            "origin": record["origin"],
            "destination": record["destination"],
            "disruption_type": record["disruption_type"],
            "summary": record.get("summary"),
            "delay_days": record.get("delay_days"),
            "risk_score": record.get("risk_score"),
            "similarity_score": round(float(normalized_scores[i]), 4)
        })

    # === Sort by similarity ===
    results = sorted(results, key=lambda x: x["similarity_score"], reverse=True)

    return {
        "query": query,
        "results": results,
        "top_k": len(results)
    }

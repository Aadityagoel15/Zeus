from fastapi import APIRouter, HTTPException
import pandas as pd
import asyncpg
import os
import faiss
import numpy as np
from tqdm import tqdm

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding, generate_summary

router = APIRouter(
    prefix="/embeddings",
    tags=["embeddings"]
)

FAISS_INDEX_PATH = "vector_search/faiss_index/shipments.index"
MAPPING_PATH = "vector_search/faiss_index/id_mapping.npy"


@router.post("/generate")
async def generate_embeddings(batch_size: int = 512, summarize: bool = False):
    """
    Generate vector embeddings (and optionally summaries) for all shipments
    and store them in FAISS + Postgres.
    """
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        records = await conn.fetch(
            "SELECT shipment_id, origin, destination, disruption_type FROM shipments"
        )
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database fetch error: {str(e)}")

    if not records:
        raise HTTPException(status_code=404, detail="No shipment records found")

    # Convert to DataFrame
    # Convert asyncpg records to DataFrame
    df = pd.DataFrame([dict(r) for r in records])

    # === Initialize FAISS index ===
    embedding_dim = 384  # for all-MiniLM-L6-v2
    index = faiss.IndexFlatL2(embedding_dim)

    all_embeddings = []
    shipment_ids = []
    summaries = []

    print(f"🧠 Generating embeddings for {len(df)} shipments...")

    # === Process in batches ===
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df.iloc[i:i + batch_size]
        texts = (batch["origin"] + " " + batch["destination"] + " " + batch["disruption_type"]).tolist()

        # Generate embeddings (batch inference)
        batch_embeddings = get_text_embedding(texts)
        all_embeddings.append(batch_embeddings)
        shipment_ids.extend(batch["shipment_id"].tolist())

        # Optional: Generate summaries
        if summarize:
            batch_summaries = [generate_summary(text) for text in texts]
            summaries.extend(batch_summaries)

    # === Concatenate embeddings ===
    all_embeddings = np.vstack(all_embeddings).astype("float32")

    # === Add to FAISS index ===
    index.add(all_embeddings)

    # === Save FAISS index + mapping ===
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)
    np.save(MAPPING_PATH, np.array(shipment_ids))

    # === Optionally store summaries in Postgres ===
    if summarize:
        try:
            conn = await asyncpg.connect(**DATABASE_CONFIG)
            for sid, summ in zip(shipment_ids, summaries):
                await conn.execute(
                    "UPDATE shipments SET summary = $1 WHERE shipment_id = $2",
                    summ, sid
                )
            await conn.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to store summaries: {str(e)}")

    return {
        "status": "success",
        "num_embeddings": len(all_embeddings),
        "summaries_stored": summarize
    }

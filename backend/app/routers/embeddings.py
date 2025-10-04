from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel
import pandas as pd
import asyncpg
import os
import faiss
import numpy as np
from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding, generate_summary  #embedding model

router = APIRouter(
    prefix = '/embeddings',
    tags = ["embeddings"]
)

FAISS_INDEX_PATH = "vector_search/faiss_index/shipments.index"
MAPPING_PATH = "vector_search/faiss_index/id_mapping.npy"

@router.post("/generate")
async def generate_embeddings(batch_size: int = 1000):
    #Fetch shipments from Postgres, generate embeddings, and store in FAISS
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        records = await conn.fetch("SELECT shipment_id, origin, destination, disruption_type FROM shipments")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
    if not records:
        raise HTTPException(status_code=404, detail="No shipment records found")
    
    df = pd.DataFrame(records, columns=['shipment_id', 'origin', 'destination', 'disruption_type'])

    #create FAISS index
    embedding_dim = 768
    index = faiss.IndexFlatL2(embedding_dim)

    embeddings_list = []
    shipment_ids = []

    # Generate embeddings in batches
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        texts = (batch['origin'] + " " + batch['destination'] + " " + batch['disruption_type']).tolist()

        batch_embeddings = [get_text_embedding(text) for text in texts]    #returns list of np.array
        embeddings_list.extend(batch_embeddings)
        shipment_ids.extend(batch['shipment_id'].tolist())

    # Convert to numpy array and add to FAISS
    embeddings_array = np.array(embeddings_list).astype('float32')
    index.add(embeddings_array)

    # Save FAISS index
    os.makedirs(os.path.dirname(FAISS_INDEX_PATH), exist_ok=True)
    faiss.write_index(index, FAISS_INDEX_PATH)

    # Save mapping: FAISS idx → shipment_id
    np.save(MAPPING_PATH, np.array(shipment_ids))

    return {"status": "success", "num_embeddings": len(embeddings_list)}

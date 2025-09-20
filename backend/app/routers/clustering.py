from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import asyncpg
import numpy as np
import os
from sklearn.cluster import KMeans

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding  # embedding model

router = APIRouter(
    prefix="/clustering",
    tags=["clustering"],
)

@router.get("/")
async def cluster_shipments(
    num_clusters: int = Query(5, description="Number of clusters to form"),
):
    # Cluster shipments based on embeddings and return cluster summaries.
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        records = await conn.fetch("SELECT shipment_id, origin, destination, disruption_type FROM shipments")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
    
    if not records:
        raise HTTPException(status_code=404, detail="No shipment records found")
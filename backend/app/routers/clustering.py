from fastapi import APIRouter, HTTPException, Query
import pandas as pd
import asyncpg
import numpy as np
import os
from sklearn.cluster import KMeans

from ..config import DATABASE_CONFIG
from ..services.summarizer import get_text_embedding, generate_summary # embedding model

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

    # convert text to embeddings
    texts = [f"{r['origin']} {r['destination']} {r['disruption_type']}" for r in records]
    embeddings = np.array([await get_text_embedding(t) for t in texts])

    # K means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init="auto")
    labels = kmeans.fit_predict(embeddings)

    clusters = {}
    for i, record in enumerate(records):
        cluster_id = int(labels[i])
        if cluster_id not in clusters:
            clusters[cluster_id] = {"shipments": [], "texts": []}
        clusters[cluster_id]["shipments"].append(dict(record))
        clusters[cluster_id]["texts"].append(texts[i])

    # generate summaries per clusters
    cluster_results = []
    for cluster_id, data in clusters.items():
        summary = await generate_summary(data["texts"])
        cluster_results.append({
            "cluster_id": cluster_id,
            "num_shipments": len(data["shipments"]),
            "summary": summary,
            "shipments": data["shipments"]
        })

    return {
        "num_clusters": num_clusters,
        "clusters": cluster_results
    }
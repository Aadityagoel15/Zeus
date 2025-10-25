from fastapi import APIRouter, HTTPException
import asyncpg
import pandas as pd
import numpy as np
from ..config import DATABASE_CONFIG
from ..services.analytics import compute_metrics

router = APIRouter(prefix="/insights", tags=["insights"])

@router.get("/metrics")
async def get_insights():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("""
            SELECT 
                origin,
                destination,
                delay_days,
                disruption_type,
                risk_score,
                route_risk_score,
                delay_severity,
                timestamp
            FROM shipments
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
    
    if not rows:
        raise HTTPException(status_code=404, detail="No shipment records found")
    
    df = pd.DataFrame([dict(r) for r in rows])
    return compute_metrics(df)


# ✅ 1. Risk Heatmap Data
@router.get("/heatmap")
async def get_heatmap_data():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("""
            SELECT origin AS location, AVG(risk_score) AS avg_risk
            FROM shipments
            GROUP BY origin
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    data = [dict(r) for r in rows]
    return {"locations": data}


# ✅ 2. Trends Over Time
@router.get("/trends")
async def get_trends_data():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("""
            SELECT 
                DATE_TRUNC('month', timestamp) AS month,
                AVG(risk_score) AS avg_risk
            FROM shipments
            GROUP BY month
            ORDER BY month
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    df = pd.DataFrame([dict(r) for r in rows])
    df["month"] = df["month"].dt.strftime("%b")
    return df.to_dict(orient="records")


# ✅ 3. Root Cause Analysis (simple NLP summary)
@router.get("/root-cause")
async def get_root_cause():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("""
            SELECT disruption_type
            FROM shipments
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not rows:
        raise HTTPException(status_code=404, detail="No disruptions found")

    df = pd.DataFrame([dict(r) for r in rows])
    top_cause = df["disruption_type"].value_counts().idxmax()
    return {"cause": f"Most frequent disruption cause: {top_cause}"}

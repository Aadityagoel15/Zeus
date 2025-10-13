from fastapi import APIRouter, HTTPException
import asyncpg
import pandas as pd
import numpy as np
from ..config import DATABASE_CONFIG
from ..services.analytics import compute_metrics

router = APIRouter(
    prefix="/insights",
    tags=["insights"],
)

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
                delay_severity
            FROM shipments
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")
    
    if not rows:
        raise HTTPException(status_code=404, detail="No shipment records found")
    
    df = pd.DataFrame([dict(r) for r in rows])

    return compute_metrics(df)
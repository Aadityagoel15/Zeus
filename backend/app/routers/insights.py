from fastapi import APIRouter, HTTPException
import asyncpg
import pandas as pd
import numpy as np
from ..config import DATABASE_CONFIG

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
    
    df = pd.DataFrame(rows)

    # Handle missing values
    df['delay_days'] = pd.to_numeric(df['delay_days'], errors='coerce').fillna(0)
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce').fillna(0)
    df['route_risk_score'] = pd.to_numeric(df['route_risk_score'], errors='coerce').fillna(0)

    total_shipments = len(df)
    avg_delay = round(df['delay_days'].mean(), 2)
    avg_risk_score = round(df['risk_score'].mean(), 2)
    delayed_ratio = round((df['delay_days'] > 0).sum() / total_shipments * 100, 2)

    # Top risky routes
    top_routes = (
        df.groupby(['origin', 'destination'])['route_risk_score']
        .mean()
        .reset_index()
        .sort_values(by='route_risk_score', ascending=False)
        .head(5)
        .to_dict(orient='records')
    )

    # Delay severity breakdown
    severity_counts = (
        df['delay_severity']
        .value_counts()
        .to_dict()
    )

    return {
        "total_shipments": total_shipments,
        "average_delay_days": avg_delay,
        "average_risk_score": avg_risk_score,
        "delayed_percentage": delayed_ratio,
        "top_risky_routes": top_routes,
        "delay_severity_breakdown": severity_counts
    }

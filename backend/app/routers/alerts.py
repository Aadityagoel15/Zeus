from fastapi import APIRouter, HTTPException
import asyncpg
import numpy as np
from ..config import DATABASE_CONFIG

router = APIRouter(
    prefix="/alerts",
    tags=["alerts"],
)

@router.get("/")
async def detect_delays(threshold_days: int = 7):
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("SELECT shipment_id, origin, destination, delay_days FROM shipments")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")

    if not rows:
        raise HTTPException(status_code=404, detail="No shipment records found")
    
    delays = np.array([float(r["delay_days"]) for r in rows])
    mean_delay = delays.mean()
    std_delay = delays.std()

    anomalies = [
        dict(r)
        for r in rows
        if r["delay_days"] and float(r["delay_days"]) > mean_delay + 2 * std_delay or float(r["delay_days"]) > threshold_days
    ]

    return {
        "mean_delay": round(mean_delay, 2),
        "std_delay": round(std_delay, 2),
        "alert_threshold": threshold_days,
        "abnormal_shipments": anomalies,
        "num_alerts": len(anomalies)
    }
from fastapi import APIRouter, HTTPException
import asyncpg
import pandas as pd
import numpy as np
from ..config import DATABASE_CONFIG
from ..services.summarizer import generate_summary

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.get("/")
async def detect_alerts(threshold: float = 2.5, summarize: bool = True):
    """
    Detect abnormal shipment delays using z-score (statistical anomaly detection)
    and optionally generate AI-based summaries.
    """
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("""
            SELECT shipment_id, origin, destination, delay_days, disruption_type
            FROM shipments
        """)
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")

    if not rows:
        raise HTTPException(status_code=404, detail="No shipment data found")

    df = pd.DataFrame([dict(r) for r in rows])
    df["delay_days"] = pd.to_numeric(df["delay_days"], errors="coerce").fillna(0)

    # === Compute delay statistics ===
    mean_delay = df["delay_days"].mean()
    std_delay = df["delay_days"].std() or 1
    df["z_score"] = (df["delay_days"] - mean_delay) / std_delay

    # === Filter high-risk alerts ===
    alerts_df = df[df["z_score"] > threshold]

    if alerts_df.empty:
        return {
            "total_alerts": 0,
            "message": "No abnormal delays detected. All routes are within expected range.",
        }

    # === Aggregate alerts by route or disruption ===
    grouped = (
        alerts_df.groupby(["origin", "destination", "disruption_type"])
        .agg({"delay_days": "mean", "shipment_id": "count"})
        .reset_index()
        .rename(columns={"shipment_id": "alert_count"})
    )

    # === AI summary generation ===
    ai_summary = ""
    if summarize:
        alert_texts = [
            f"Route {row['origin']} → {row['destination']} has an average delay of {row['delay_days']:.2f} days due to {row['disruption_type']}."
            for _, row in grouped.iterrows()
        ]
        combined_text = " ".join(alert_texts)
        ai_summary = generate_summary(combined_text)

    # === Format response ===
    return {
        "total_alerts": len(alerts_df),
        "mean_delay": round(mean_delay, 2),
        "std_dev": round(std_delay, 2),
        "alert_summary": ai_summary if summarize else None,
        "alert_details": grouped.to_dict(orient="records"),
    }

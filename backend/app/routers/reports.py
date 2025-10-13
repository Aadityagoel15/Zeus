from fastapi import APIRouter, HTTPException, Response
import asyncpg
import pandas as pd
import io
from ..config import DATABASE_CONFIG

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/csv")
async def download_report():
    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("SELECT * FROM shipments")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")

    if not rows:
        raise HTTPException(status_code=404, detail="No data found")

    # Convert asyncpg records to DataFrame
    df = pd.DataFrame([dict(r) for r in rows])

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return Response(
        content=buffer.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=shipment_report.csv"}
    )

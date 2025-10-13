from fastapi import APIRouter, HTTPException, Query
import asyncpg
import pandas as pd
from ..config import DATABASE_CONFIG

router = APIRouter(prefix="/recommendations", tags=["recommendations"])

# Custom recommendations mapped to disruption types
DISRUPTION_RECOMMENDATIONS = {
    "Shortage": "Improve inventory forecasting and supplier communication to avoid stockouts.",
    "Weather": "Implement better weather forecasting and flexible routing to minimize impact.",
    "Customs": "Streamline customs paperwork and build relationships with brokers to reduce delays.",
    "Strike": "Develop contingency labor plans and diversify workforce sources to mitigate strike effects.",
}


@router.get("/")
async def get_recommendations(
    route_limit: int = Query(5, description="Number of top delayed routes to show"),
    disruption_limit: int = Query(3, description="Number of top disruptions to show")
):
    """
    Returns data-driven supply chain recommendations.
    You can customize the number of insights with query params:
    - /recommendations?route_limit=10&disruption_limit=5
    """

    try:
        conn = await asyncpg.connect(**DATABASE_CONFIG)
        rows = await conn.fetch("SELECT origin, destination, disruption_type, delay_days FROM shipments")
        await conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB fetch error: {str(e)}")

    if not rows:
        raise HTTPException(status_code=404, detail="No shipment records found")

    df = pd.DataFrame(rows)
    insights = []

    # Analyze delays by route
    if "delay_days" in df.columns:
        high_delay_routes = (
            df.groupby(["origin", "destination"])["delay_days"]
            .mean()
            .reset_index()
            .sort_values(by="delay_days", ascending=False)
            .head(route_limit)
        )
        for _, row in high_delay_routes.iterrows():
            insights.append({
                "route": f"{row['origin']} → {row['destination']}",
                "avg_delay": round(row['delay_days'], 2),
                "recommendation": "Consider alternate routes or partner carriers to reduce consistent delays."
            })

    # Analyze disruption types with custom recommendations
    if "disruption_type" in df.columns:
        top_disruptions = df["disruption_type"].value_counts().head(disruption_limit).to_dict()
        for disruption, frequency in top_disruptions.items():
            recommendation = DISRUPTION_RECOMMENDATIONS.get(
                disruption,
                f"Investigate and mitigate frequent '{disruption}' disruptions."
            )
            insights.append({
                "disruption": disruption,
                "frequency": frequency,
                "recommendation": recommendation
            })

    return {
        "total_recommendations": len(insights),
        "recommendations": insights
    }

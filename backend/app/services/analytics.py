import pandas as pd

def compute_metrics(df: pd.DataFrame):
    df['delay_days'] = pd.to_numeric(df['delay_days'], errors='coerce').fillna(0)
    df['risk_score'] = pd.to_numeric(df['risk_score'], errors='coerce').fillna(0)
    df['route_risk_score'] = pd.to_numeric(df['route_risk_score'], errors='coerce').fillna(0)

    total_shipments = len(df)
    avg_delay = round(df['delay_days'].mean(), 2)
    avg_risk_score = round(df['risk_score'].mean(), 2)
    delayed_ratio = round((df['delay_days'] > 0).sum() / total_shipments * 100, 2)

    top_routes = (
        df.groupby(['origin', 'destination'])['route_risk_score']
        .mean()
        .reset_index()
        .sort_values(by='route_risk_score', ascending=False)
        .head(5)
        .to_dict(orient='records')
    )

    severity_counts = df['delay_severity'].value_counts().to_dict()

    return {
        "total_shipments": total_shipments,
        "average_delay_days": avg_delay,
        "average_risk_score": avg_risk_score,
        "delayed_percentage": delayed_ratio,
        "top_risky_routes": top_routes,
        "delay_severity_breakdown": severity_counts
    }

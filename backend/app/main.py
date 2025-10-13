# backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Supply Chain Alert System API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers after FastAPI app is created (avoid circular imports)
try:
    from .routers import alerts, insights, clustering, embeddings, search, recommendations, reports
    
    # Include all routers
    app.include_router(alerts.router)
    app.include_router(insights.router)
    app.include_router(clustering.router)
    app.include_router(embeddings.router)
    app.include_router(search.router)
    app.include_router(recommendations.router)
    app.include_router(reports.router)
    
except Exception as e:
    print(f"❌ Error importing routers: {e}")
    import traceback
    traceback.print_exc()

# Root endpoint
@app.get("/")
def root():
    return {"message": "Supply Chain Alert System API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="127.0.0.1", port=8000, reload=True)
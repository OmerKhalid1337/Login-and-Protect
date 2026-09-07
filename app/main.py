from fastapi import FastAPI
from app.config import SUPABASE_URL, SUPABASE_KEY, supabase

app = FastAPI(
    title="Auth Login & Protect API",
    description="A secure FastAPI authentication backend integrated with Supabase Auth.",
    version="1.0.0",
)

@app.get("/", tags=["Health Check"])
def root():
    """Health check endpoint to verify server status and Supabase connection readiness."""
    supabase_configured = bool(SUPABASE_URL and SUPABASE_KEY and supabase is not None)
    return {
        "status": "online",
        "message": "Auth Login & Protect API is running.",
        "supabase_configured": supabase_configured,
    }

if __name__ == "__main__":
    import uvicorn
    from app.config import PORT, HOST
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)

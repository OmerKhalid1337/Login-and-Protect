from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.config import SUPABASE_URL, SUPABASE_KEY, supabase
from app.routers import auth, public, protected

tags_metadata = [
    {
        "name": "Public",
        "description": "Endpoints accessible by anyone without authentication.",
    },
    {
        "name": "Authentication",
        "description": "User registration (`/signup`), login (`/login`), and authenticated logout (`/logout`).",
    },
    {
        "name": "Protected",
        "description": "Secured endpoints requiring a valid Supabase JWT Bearer token.",
    },
    {
        "name": "Health Check",
        "description": "System health and Supabase connection readiness.",
    },
]

app = FastAPI(
    title="Auth Login & Protect API",
    description="""
# Auth Login & Protect API (FlyRank Backend Track - Assignment A4)

A secure backend REST API integrated with **Supabase Auth** as the Identity Provider (IdP).

## Authentication Flow:
1. **Register**: Send email and password to `POST /auth/signup`.
2. **Log in**: Send credentials to `POST /auth/login` to receive your **JWT Access Token**.
3. **Authorize in Swagger**: Click the **Authorize 🔓** button at the top right, paste your JWT token, and click **Authorize**.
4. **Access Protected Routes**: Test `GET /protected/profile`, `GET /protected/dashboard`, or `POST /auth/logout`.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Ensure HTTP error responses match the exact JSON error format specified in the assignment."""
    if isinstance(exc.detail, dict) and "error" in exc.detail:
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    if isinstance(exc.detail, str):
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Ensure missing or invalid request bodies return HTTP 400 Bad Request per assignment spec."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Missing or invalid request payload", "details": exc.errors()},
    )

# Include routers
app.include_router(public.router)
app.include_router(auth.router)
app.include_router(protected.router)

@app.get("/", tags=["Health Check"], summary="Server Health Check")
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

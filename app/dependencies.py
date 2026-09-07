from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from app.config import supabase

# HTTPBearer with auto_error=False allows us to provide exact assignment-specified JSON error messages
bearer_scheme = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> Dict[str, Any]:
    """
    Reusable authentication dependency (guard) for FastAPI protected routes.
    1. Validates the presence and format of Authorization: Bearer <token>.
    2. Rejects missing/malformed tokens with 401 {"error": "Access token required"}.
    3. Calls Supabase Auth to cryptographically verify the JWT.
    4. Rejects invalid/expired/tampered tokens with 401 {"error": "Invalid or expired token"}.
    5. Returns the verified user payload to the route handler.
    """
    if not credentials or not credentials.credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )

    token = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )

    if supabase is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Supabase client is not configured"}
        )

    try:
        user_response = supabase.auth.get_user(token)
        user = user_response.user

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"}
            )

        return {
            "id": user.id,
            "email": user.email,
            "created_at": str(user.created_at) if user.created_at else None,
            "app_metadata": user.app_metadata,
            "user_metadata": user.user_metadata,
            "token": token,
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )

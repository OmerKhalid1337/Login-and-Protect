from fastapi import APIRouter, Header, HTTPException, status
from typing import Optional
from app.config import supabase

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(authorization: Optional[str] = Header(None)):
    """
    Stage 3 verified protected route:
    - Extracts the Bearer token from Authorization header.
    - Verifies the token cryptographically via Supabase Auth (get_user).
    - Rejects missing/malformed header with 401 {"error": "Access token required"}.
    - Rejects invalid/expired/tampered tokens with 401 {"error": "Invalid or expired token"}.
    - Returns authenticated user metadata (id, email, created_at) on success.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )

    parts = authorization.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"}
        )

    token = parts[1]

    if supabase is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Supabase client is not configured"}
        )

    try:
        # Live token verification with Supabase
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
        }

    except HTTPException:
        raise
    except Exception:
        # Any verification failure (tampered, expired, fake token) returns 401
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"}
        )

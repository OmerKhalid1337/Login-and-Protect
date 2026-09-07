from fastapi import APIRouter, Header, HTTPException, status
from typing import Optional

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(authorization: Optional[str] = Header(None)):
    """
    Stage 2 unverified protected route:
    - Checks for the presence of Authorization: Bearer <token>
    - Rejects missing, malformed, or empty tokens with 401 Unauthorized
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
    # Unverified stage: proves header parsing and gate check
    return {
        "message": "Token presented successfully (unverified stage)",
        "token_preview": f"{token[:10]}..." if len(token) > 10 else token
    }

from fastapi import APIRouter, Depends, status
from typing import Dict, Any
from app.dependencies import get_current_user

router = APIRouter(prefix="/protected", tags=["Protected"])

@router.get("/profile", status_code=status.HTTP_200_OK)
def get_profile(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Protected user profile route guarded by get_current_user dependency.
    Returns the authenticated user's private metadata.
    """
    return {
        "id": current_user["id"],
        "email": current_user["email"],
        "created_at": current_user["created_at"],
        "app_metadata": current_user["app_metadata"],
        "user_metadata": current_user["user_metadata"],
    }

@router.get("/dashboard", status_code=status.HTTP_200_OK)
def get_dashboard(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Second protected route proving that the authentication dependency is reusable.
    """
    return {
        "message": f"Welcome to your private dashboard, {current_user['email']}!",
        "user_id": current_user["id"],
        "status": "authenticated",
    }

from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from typing import Dict, Any
from app.config import supabase
from app.schemas import AuthCredentials
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: AuthCredentials):
    """
    Register a new user account with Supabase Auth.
    - Missing or empty email/password returns 400 Bad Request.
    - Successful registration returns 201 Created with user info.
    """
    if not credentials.email or not credentials.email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email is required"}
        )
    if not credentials.password or not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Password is required"}
        )

    if supabase is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Supabase client is not configured"}
        )

    try:
        response = supabase.auth.sign_up({
            "email": credentials.email.strip(),
            "password": credentials.password
        })

        if not response.user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Failed to create user account"}
            )

        user_data = {
            "id": response.user.id,
            "email": response.user.email,
            "created_at": str(response.user.created_at) if response.user.created_at else None,
            "app_metadata": response.user.app_metadata,
            "user_metadata": response.user.user_metadata,
        }

        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"user": user_data})

    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error_msg}
        )

@router.post("/login", status_code=status.HTTP_200_OK)
def login(credentials: AuthCredentials):
    """
    Authenticate an existing user with Supabase Auth and return access & refresh tokens.
    - Missing or empty fields return 400 Bad Request.
    - Invalid credentials return 401 Unauthorized.
    - Successful login returns 200 OK with tokens.
    """
    if not credentials.email or not credentials.email.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email is required"}
        )
    if not credentials.password or not credentials.password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Password is required"}
        )

    if supabase is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Supabase client is not configured"}
        )

    try:
        response = supabase.auth.sign_in_with_password({
            "email": credentials.email.strip(),
            "password": credentials.password
        })

        if not response.session or not response.session.access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid login credentials"}
            )

        user_data = None
        if response.user:
            user_data = {
                "id": response.user.id,
                "email": response.user.email,
                "created_at": str(response.user.created_at) if response.user.created_at else None,
            }

        return {
            "access_token": response.session.access_token,
            "token_type": "bearer",
            "refresh_token": response.session.refresh_token,
            "user": user_data
        }

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials"}
        )

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Log out the authenticated user.
    - Protected endpoint requiring a valid Bearer token.
    - Calls Supabase Auth to invalidate session.
    - Returns 204 No Content on success.
    """
    if supabase is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Supabase client is not configured"}
        )

    try:
        supabase.auth.sign_out()
    except Exception:
        # Even if remote session was already expired locally, the signout request succeeded
        pass

    return Response(status_code=status.HTTP_204_NO_CONTENT)

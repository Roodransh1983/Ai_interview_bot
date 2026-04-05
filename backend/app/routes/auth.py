"""
Authentication routes — /auth/*
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.models.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth_service import AuthService
from app.utils.security import decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> UserResponse:
    """Dependency to get current authenticated user from JWT"""
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    auth_service = AuthService(db)
    try:
        user = await auth_service.get_user_by_id(payload["sub"])
        return user
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )


@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Register a new user account"""
    auth_service = AuthService(db)
    try:
        result = await auth_service.register(user_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: AsyncIOMotorDatabase = Depends(get_db)):
    """Login with email and password"""
    auth_service = AuthService(db)
    try:
        result = await auth_service.login(user_data.email, user_data.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """Get current user info"""
    return current_user

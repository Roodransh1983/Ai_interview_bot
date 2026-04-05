"""
Authentication service — business logic for user registration and login
"""
from datetime import datetime
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.models.user import UserRegister, UserResponse, TokenResponse
from app.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users

    async def register(self, user_data: UserRegister) -> TokenResponse:
        """Register a new user"""
        # Check if email already exists
        existing = await self.collection.find_one({"email": user_data.email})
        if existing:
            raise ValueError("Email already registered")

        # Hash password and create user doc
        user_doc = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hash_password(user_data.password),
            "created_at": datetime.utcnow(),
            "resume_uploaded": False,
            "resume_data": None,
            "total_interviews": 0,
            "avg_score": 0.0,
        }

        result = await self.collection.insert_one(user_doc)
        user_id = str(result.inserted_id)

        # Generate JWT token
        token = create_access_token({"sub": user_id, "email": user_data.email})

        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user_id,
                name=user_data.name,
                email=user_data.email,
                created_at=user_doc["created_at"],
            ),
        )

    async def login(self, email: str, password: str) -> TokenResponse:
        """Authenticate user and return token"""
        user = await self.collection.find_one({"email": email})
        if not user or not verify_password(password, user["password"]):
            raise ValueError("Invalid email or password")

        user_id = str(user["_id"])
        token = create_access_token({"sub": user_id, "email": user["email"]})

        return TokenResponse(
            access_token=token,
            user=UserResponse(
                id=user_id,
                name=user["name"],
                email=user["email"],
                created_at=user["created_at"],
                resume_uploaded=user.get("resume_uploaded", False),
                total_interviews=user.get("total_interviews", 0),
                avg_score=user.get("avg_score", 0.0),
            ),
        )

    async def get_user_by_id(self, user_id: str) -> UserResponse:
        """Get user by ID"""
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise ValueError("User not found")

        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            created_at=user["created_at"],
            resume_uploaded=user.get("resume_uploaded", False),
            total_interviews=user.get("total_interviews", 0),
            avg_score=user.get("avg_score", 0.0),
        )

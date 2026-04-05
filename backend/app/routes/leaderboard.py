"""
Leaderboard routes
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import UserResponse

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("/")
async def get_leaderboard(
    limit: int = 10,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """
    Get top users ranked by average interview score.
    Returns top N users with their average scores.
    """
    pipeline = [
        {
            "$match": {
                "total_interviews": {"$gt": 0},
                "avg_score": {"$gt": 0},
            }
        },
        {
            "$project": {
                "name": 1,
                "avg_score": {"$round": ["$avg_score", 1]},
                "total_interviews": 1,
            }
        },
        {"$sort": {"avg_score": -1}},
        {"$limit": limit},
    ]

    results = []
    async for doc in db.users.aggregate(pipeline):
        results.append({
            "rank": len(results) + 1,
            "user_id": str(doc["_id"]),
            "name": doc["name"],
            "avg_score": doc["avg_score"],
            "total_interviews": doc["total_interviews"],
        })

    return {"leaderboard": results, "total_participants": len(results)}


@router.get("/me")
async def get_my_rank(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Get current user's rank on the leaderboard"""
    # Get user's score
    user = await db.users.find_one({"_id": ObjectId(current_user.id)})
    if not user or user.get("total_interviews", 0) == 0:
        return {"rank": None, "message": "Complete an interview to appear on the leaderboard"}

    # Count users with higher average
    count = await db.users.count_documents({
        "avg_score": {"$gt": user.get("avg_score", 0)},
        "total_interviews": {"$gt": 0},
    })

    return {
        "rank": count + 1,
        "avg_score": user.get("avg_score", 0),
        "total_interviews": user.get("total_interviews", 0),
    }

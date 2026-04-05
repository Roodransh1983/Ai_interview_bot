"""
MongoDB async connection using Motor
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

client: AsyncIOMotorClient = None
db: AsyncIOMotorDatabase = None


async def connect_db():
    """Create MongoDB connection on app startup"""
    global client, db
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]

    # Create indexes
    await db.users.create_index("email", unique=True)
    await db.interviews.create_index("user_id")
    await db.leaderboard.create_index("user_id")

    print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")


async def close_db():
    """Close MongoDB connection on app shutdown"""
    global client
    if client:
        client.close()
        print("❌ MongoDB connection closed")


def get_db() -> AsyncIOMotorDatabase:
    """Get database instance"""
    return db

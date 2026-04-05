"""
Resume upload and parsing routes
"""
import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import UserResponse, ResumeData
from app.services.resume_service import ResumeService

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeData)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Upload and parse a resume (PDF or DOCX)"""
    service = ResumeService(db)

    # Validate file type
    allowed_types = [".pdf", ".docx", ".doc"]
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    if ext.lower() not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type not supported. Allowed: {', '.join(allowed_types)}",
        )

    # Create upload directory if not exists
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save file
    file_path = os.path.join(upload_dir, f"{current_user.id}_{file.filename}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        # Parse and store
        resume_data = await service.upload_and_parse(
            user_id=current_user.id,
            file_path=file_path,
            file_extension=ext,
        )
        return resume_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {str(e)}")
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/", response_model=ResumeData)
async def get_resume(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Get the current user's parsed resume data"""
    service = ResumeService(db)
    return await service.get_resume(current_user.id)

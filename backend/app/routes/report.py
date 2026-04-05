"""
Report and email routes
"""
from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import UserResponse
from app.services.interview_service import InterviewService
from app.services.email_service import EmailService

router = APIRouter(prefix="/report", tags=["Report"])


@router.get("/{report_id}")
async def get_report(
    report_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Get a specific interview report"""
    service = InterviewService(db)
    try:
        report = await service.get_report(report_id)
        # Verify ownership
        if report.get("user_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        return report
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/history/me")
async def get_my_reports(
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Get all reports for the current user"""
    service = InterviewService(db)
    return await service.get_user_reports(current_user.id)


@router.post("/{report_id}/email")
async def send_report_email(
    report_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Send the report to the user's email"""
    service = InterviewService(db)
    email_service = EmailService()

    try:
        report = await service.get_report(report_id)
        # Verify ownership
        if report.get("user_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

        success = email_service.send_report(
            to_email=current_user.email,
            report=report,
            user_name=current_user.name,
        )

        if success:
            return {"message": "Report sent to your email"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email. Check SMTP configuration.")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

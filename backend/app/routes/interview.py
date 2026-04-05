"""
Interview routes — start session, submit answers, complete interview
"""
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.database import get_db
from app.routes.auth import get_current_user
from app.models.user import UserResponse
from app.services.interview_service import InterviewService

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.post("/start")
async def start_interview(
    mode: str = "text",
    difficulty: str = "medium",
    num_questions: int = 5,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Start a new interview session"""
    service = InterviewService(db)
    try:
        return await service.start_session(
            user_id=current_user.id,
            mode=mode,
            difficulty=difficulty,
            num_questions=num_questions,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/answer")
async def submit_answer(
    session_id: str,
    question_id: str,
    answer_text: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Submit an answer for evaluation"""
    service = InterviewService(db)
    try:
        return await service.submit_answer(
            session_id=session_id,
            question_id=question_id,
            answer_text=answer_text,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete/{session_id}")
async def complete_interview(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Complete the interview and generate the final report"""
    service = InterviewService(db)
    try:
        return await service.complete_session(
            session_id=session_id,
            user_name=current_user.name,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}")
async def get_session(
    session_id: str,
    current_user: UserResponse = Depends(get_current_user),
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    """Get interview session details"""
    service = InterviewService(db)
    try:
        return await service.get_session(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# WebSocket endpoint for real-time interview (video/text)
@router.websocket("/ws")
async def interview_websocket(websocket: WebSocket):
    """
    WebSocket endpoint for real-time interview.
    Handles question flow, answer submission, and evaluation in real-time.
    """
    await websocket.accept()

    # Note: For simplicity, using a basic token validation.
    # In production, you'd validate the JWT from the query param or first message.
    try:
        # Receive auth token first
        auth_data = await websocket.receive_json()
        token = auth_data.get("token")
        if not token:
            await websocket.send_json({"type": "error", "message": "Authentication required"})
            await websocket.close()
            return

        # Validate token and get user
        from app.utils.security import decode_token
        from app.services.auth_service import AuthService

        payload = decode_token(token)
        if not payload:
            await websocket.send_json({"type": "error", "message": "Invalid token"})
            await websocket.close()
            return

        db = get_db()
        auth_service = AuthService(db)
        user = await auth_service.get_user_by_id(payload["sub"])

        # Initialize interview service
        service = InterviewService(db)

        # Receive session start config
        config_data = await websocket.receive_json()
        mode = config_data.get("mode", "text")
        difficulty = config_data.get("difficulty", "medium")
        num_questions = config_data.get("num_questions", 5)

        # Start session
        session_data = await service.start_session(
            user_id=user.id,
            mode=mode,
            difficulty=difficulty,
            num_questions=num_questions,
        )

        await websocket.send_json({
            "type": "session_started",
            "data": session_data,
        })

        # Main interview loop
        while True:
            try:
                # Receive message (answer or control)
                msg = await websocket.receive_json()
                msg_type = msg.get("type")

                if msg_type == "answer":
                    # Process answer
                    result = await service.submit_answer(
                        session_id=session_data["session_id"],
                        question_id=msg["question_id"],
                        answer_text=msg["answer"],
                    )

                    await websocket.send_json({
                        "type": "evaluation",
                        "data": result,
                    })

                    if result["has_next"]:
                        await websocket.send_json({
                            "type": "next_question",
                            "data": result["next_question"],
                        })
                    else:
                        # Interview complete
                        report = await service.complete_session(
                            session_id=session_data["session_id"],
                            user_name=user.name,
                        )
                        await websocket.send_json({
                            "type": "interview_complete",
                            "data": {"report_id": report["report_id"], **report},
                        })

                elif msg_type == "end_early":
                    # User wants to end without answering all
                    report = await service.complete_session(
                        session_id=session_data["session_id"],
                        user_name=user.name,
                    )
                    await websocket.send_json({
                        "type": "interview_complete",
                        "data": {"report_id": report["report_id"], **report},
                    })
                    break

            except WebSocketDisconnect:
                break
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "message": str(e),
                })

    except WebSocketDisconnect:
        pass
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)})
        except:
            pass

"""
Interview session management service
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import settings
from app.models.interview import InterviewSession, InterviewReport, Question, AnswerEvaluation
from ai_engine.question_generator import QuestionGenerator
from ai_engine.answer_evaluator import AnswerEvaluator
from ai_engine.scoring_engine import ScoringEngine


class InterviewService:
    """Manages interview sessions, question generation, and answer evaluation"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.sessions_collection = db.interviews
        self.reports_collection = db.reports
        self.users_collection = db.users
        self.question_gen = QuestionGenerator()
        self.evaluator = AnswerEvaluator()
        self.scorer = ScoringEngine()

    async def start_session(
        self,
        user_id: str,
        mode: str = "text",
        difficulty: str = "medium",
        num_questions: int = 5,
    ) -> Dict:
        """
        Start a new interview session for a user.
        Generates questions based on their resume skills.
        """
        # Get user's resume skills
        user = await self.users_collection.find_one({"_id": ObjectId(user_id)})
        resume_skills = []
        if user and user.get("resume_data", {}).get("skills"):
            resume_skills = user["resume_data"]["skills"]

        # Generate questions based on resume skills
        questions = self.question_gen.generate(
            resume_skills=resume_skills,
            num_questions=num_questions or settings.QUESTIONS_PER_INTERVIEW,
            difficulty=difficulty,
            include_hr=True,
        )

        # Convert to Question objects
        question_objs = [
            Question(
                id=q["id"],
                text=q["text"],
                category=q["category"],
                difficulty=q["difficulty"],
                ideal_keywords=q["ideal_keywords"],
                ideal_answer=q["ideal_answer"],
            )
            for q in questions
        ]

        # Create session
        session_id = str(uuid.uuid4())
        session = InterviewSession(
            id=session_id,
            user_id=user_id,
            mode=mode,
            difficulty=difficulty,
            questions=question_objs,
            answers=[],
            scores=[],
            confidence_scores=[],
            started_at=datetime.utcnow(),
        )

        # Store session in DB
        await self.sessions_collection.insert_one(session.model_dump())

        # Return first question with metadata
        first_q = question_objs[0]
        return {
            "session_id": session_id,
            "total_questions": len(question_objs),
            "current_question": {
                "id": first_q.id,
                "text": first_q.text,
                "category": first_q.category,
                "difficulty": first_q.difficulty,
                "number": 1,
                "time_limit": settings.QUESTION_TIME_SECONDS,
            },
        }

    async def submit_answer(
        self,
        session_id: str,
        question_id: str,
        answer_text: str,
    ) -> Dict:
        """
        Submit an answer for evaluation.
        Returns the evaluation result and next question (if any).
        """
        # Get session
        session_doc = await self.sessions_collection.find_one({"id": session_id})
        if not session_doc:
            raise ValueError("Session not found")

        # Find the question
        questions = session_doc["questions"]
        current_idx = len(session_doc["answers"])
        question = questions[current_idx]

        if question["id"] != question_id:
            raise ValueError("Question ID mismatch")

        # Evaluate answer using AI engine
        evaluation = self.evaluator.evaluate(
            user_answer=answer_text,
            ideal_answer=question["ideal_answer"],
            ideal_keywords=question["ideal_keywords"],
            question_category=question["category"],
        )

        # Update session
        await self.sessions_collection.update_one(
            {"id": session_id},
            {
                "$push": {
                    "answers": answer_text,
                    "scores": evaluation["score"],
                    "confidence_scores": evaluation["confidence_score"],
                }
            },
        )

        # Check if more questions remain
        next_idx = current_idx + 1
        has_next = next_idx < len(questions)

        next_question_data = None
        if has_next:
            next_q = questions[next_idx]
            next_question_data = {
                "id": next_q["id"],
                "text": next_q["text"],
                "category": next_q["category"],
                "difficulty": next_q["difficulty"],
                "number": next_idx + 1,
                "time_limit": settings.QUESTION_TIME_SECONDS,
            }

        return {
            "evaluation": evaluation,
            "question_number": current_idx + 1,
            "total_questions": len(questions),
            "has_next": has_next,
            "next_question": next_question_data,
        }

    async def complete_session(self, session_id: str, user_name: str = "Candidate") -> Dict:
        """
        Complete the interview session and generate the final report.
        """
        # Get session
        session_doc = await self.sessions_collection.find_one({"id": session_id})
        if not session_doc:
            raise ValueError("Session not found")

        # Build answer data with full question info for the report
        answers_data = []
        questions = session_doc["questions"]
        for i, answer in enumerate(session_doc["answers"]):
            q = questions[i]
            evaluation = self.evaluator.evaluate(
                user_answer=answer,
                ideal_answer=q["ideal_answer"],
                ideal_keywords=q["ideal_keywords"],
                question_category=q["category"],
            )
            answers_data.append({
                "question": q["text"],
                "user_answer": answer,
                "score": evaluation["score"],
                "confidence_score": evaluation["confidence_score"],
                "category": q["category"],
                "feedback": evaluation["feedback"],
                "keywords_matched": evaluation["keywords_matched"],
                "keywords_missed": evaluation["keywords_missed"],
            })

        # Generate report
        report = self.scorer.generate_report(answers_data, user_name)

        # Store report
        report_id = str(uuid.uuid4())
        report_doc = {
            "id": report_id,
            "session_id": session_id,
            "user_id": session_doc["user_id"],
            **report,
            "created_at": datetime.utcnow(),
        }
        await self.reports_collection.insert_one(report_doc)

        # Update session with report_id and completion time
        await self.sessions_collection.update_one(
            {"id": session_id},
            {
                "$set": {
                    "completed_at": datetime.utcnow(),
                    "total_score": report["total_score"],
                    "report_id": report_id,
                }
            },
        )

        # Update user stats
        await self._update_user_stats(session_doc["user_id"])

        return {
            "report_id": report_id,
            **report,
        }

    async def get_report(self, report_id: str) -> Dict:
        """Get a specific interview report"""
        report = await self.reports_collection.find_one({"id": report_id})
        if not report:
            raise ValueError("Report not found")
        # Remove MongoDB _id
        report.pop("_id", None)
        return report

    async def get_user_reports(self, user_id: str) -> List[Dict]:
        """Get all reports for a user"""
        reports = []
        cursor = self.reports_collection.find({"user_id": user_id}).sort("created_at", -1)
        async for report in cursor:
            report.pop("_id", None)
            reports.append(report)
        return reports

    async def get_session(self, session_id: str) -> Dict:
        """Get interview session details"""
        session = await self.sessions_collection.find_one({"id": session_id})
        if not session:
            raise ValueError("Session not found")
        session.pop("_id", None)
        return session

    async def _update_user_stats(self, user_id: str):
        """Update user's interview statistics"""
        pipeline = [
            {"$match": {"user_id": user_id, "total_score": {"$exists": True}}},
            {
                "$group": {
                    "_id": "$user_id",
                    "total_interviews": {"$sum": 1},
                    "avg_score": {"$avg": "$total_score"},
                }
            },
        ]
        async for result in self.users_collection.aggregate(pipeline):
            await self.users_collection.update_one(
                {"_id": ObjectId(user_id)},
                {
                    "$set": {
                        "total_interviews": result["total_interviews"],
                        "avg_score": round(result["avg_score"], 1),
                    }
                },
            )
            break

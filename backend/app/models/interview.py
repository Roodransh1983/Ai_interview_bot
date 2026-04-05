"""
Interview session models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Question(BaseModel):
    id: str
    text: str
    category: str
    difficulty: str  # easy, medium, hard
    ideal_keywords: List[str]
    ideal_answer: str


class AnswerSubmission(BaseModel):
    question_id: str
    answer_text: str


class AnswerEvaluation(BaseModel):
    score: float = Field(..., ge=0, le=100)
    feedback: str
    keywords_matched: List[str]
    keywords_missed: List[str]
    confidence_score: float
    correct: bool


class InterviewSession(BaseModel):
    id: str
    user_id: str
    mode: str  # text or video
    difficulty: str
    questions: List[Question]
    answers: List[str]
    scores: List[float]
    confidence_scores: List[float]
    started_at: datetime
    completed_at: Optional[datetime] = None
    total_score: float = 0.0
    report_id: Optional[str] = None


class InterviewReport(BaseModel):
    id: str
    session_id: str
    user_id: str
    total_score: float
    answer_evaluations: List[AnswerEvaluation]
    strengths: List[str]
    weaknesses: List[str]
    suggestions: List[str]
    category_scores: dict  # category -> avg score
    created_at: datetime

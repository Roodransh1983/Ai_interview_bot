"""
Scoring Engine — aggregates scores, identifies strengths/weaknesses, generates reports
"""
from typing import List, Dict, Tuple
from collections import defaultdict


class ScoringEngine:
    """Aggregates interview scores and generates comprehensive reports"""

    def generate_report(
        self,
        answers: List[Dict],  # List of {question, user_answer, score, confidence_score, category}
        user_name: str = "Candidate",
    ) -> Dict:
        """
        Generate a comprehensive interview report.

        Args:
            answers: List of answer evaluation results with category info
            user_name: Name of the candidate

        Returns:
            Report dict with total score, strengths, weaknesses, suggestions
        """
        if not answers:
            return self._empty_report(user_name)

        # Calculate total score (weighted average of answer and confidence scores)
        total_answer_score = sum(a["score"] for a in answers)
        total_confidence = sum(a["confidence_score"] for a in answers)
        total_score = round((total_answer_score + total_confidence) / 2, 1)

        # Score by category
        category_scores = defaultdict(list)
        for answer in answers:
            category_scores[answer["category"]].append(answer["score"])

        category_averages = {
            cat: round(sum(scores) / len(scores), 1)
            for cat, scores in category_scores.items()
        }

        # Identify strengths (categories with avg score >= 70)
        strengths = [
            cat for cat, avg in category_averages.items()
            if avg >= 70 and cat != "HR"
        ]

        # Identify weaknesses (categories with avg score < 60)
        weaknesses = [
            cat for cat, avg in category_averages.items()
            if avg < 60 and cat != "HR"
        ]

        # Generate suggestions based on weaknesses
        suggestions = self._generate_suggestions(weaknesses, answers)

        # Build per-question breakdown
        breakdown = []
        for i, answer in enumerate(answers):
            breakdown.append({
                "question_number": i + 1,
                "question": answer.get("question", ""),
                "category": answer.get("category", "Unknown"),
                "user_answer": answer.get("user_answer", ""),
                "score": answer.get("score", 0),
                "confidence_score": answer.get("confidence_score", 0),
                "feedback": answer.get("feedback", ""),
                "keywords_matched": answer.get("keywords_matched", []),
                "keywords_missed": answer.get("keywords_missed", []),
            })

        return {
            "user_name": user_name,
            "total_score": total_score,
            "category_scores": category_averages,
            "strengths": strengths if strengths else ["General communication"],
            "weaknesses": weaknesses if weaknesses else [],
            "suggestions": suggestions,
            "breakdown": breakdown,
            "total_questions": len(answers),
            "average_answer_score": round(total_answer_score / len(answers), 1),
            "average_confidence": round(total_confidence / len(answers), 1),
            "grade": self._get_grade(total_score),
        }

    def _generate_suggestions(
        self, weaknesses: List[str], answers: List[Dict]
    ) -> List[str]:
        """Generate specific improvement suggestions based on weak categories"""
        suggestions = []
        suggestion_map = {
            "Python": "Practice Python fundamentals including decorators, generators, and memory management. Build small projects to reinforce concepts.",
            "JavaScript": "Strengthen your JavaScript skills by understanding closures, the event loop, and ES6+ features. Build interactive web projects.",
            "React": "Focus on React hooks (useState, useEffect, useCallback, useMemo) and understanding the Virtual DOM reconciliation process.",
            "Node.js": "Learn Express.js middleware patterns, asynchronous programming patterns, and Node.js internals like the event loop.",
            "SQL": "Practice complex JOIN queries, subqueries, and database normalization. Work on optimizing slow queries.",
            "Machine Learning": "Review supervised vs unsupervised learning, overfitting prevention techniques, and model evaluation metrics.",
            "Data Structures": "Practice implementing and using arrays, linked lists, trees, hash tables, and graphs. Solve algorithmic problems.",
            "Java": "Review OOP principles, Java collections framework, and multithreading concepts. Understand JVM basics.",
            "HR": "Practice structured responses using the STAR method (Situation, Task, Action, Result) for behavioral questions.",
        }

        for weakness in weaknesses[:3]:  # Top 3 weaknesses
            if weakness in suggestion_map:
                suggestions.append(suggestion_map[weakness])
            else:
                suggestions.append(
                    f"Strengthen your {weakness} knowledge through hands-on practice and project work."
                )

        # Add general suggestions if few specific ones
        if len(suggestions) < 2:
            suggestions.append(
                "Practice explaining technical concepts clearly and concisely."
            )
            suggestions.append(
                "Work on providing specific examples from your experience when answering questions."
            )

        return suggestions[:5]  # Max 5 suggestions

    def _get_grade(self, score: float) -> str:
        """Convert numeric score to letter grade"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C"
        elif score >= 50:
            return "D"
        else:
            return "F"

    def _empty_report(self, user_name: str) -> Dict:
        """Return an empty report structure"""
        return {
            "user_name": user_name,
            "total_score": 0.0,
            "category_scores": {},
            "strengths": [],
            "weaknesses": [],
            "suggestions": [],
            "breakdown": [],
            "total_questions": 0,
            "average_answer_score": 0.0,
            "average_confidence": 0.0,
            "grade": "F",
        }

    def compare_with_previous(self, current_score: float, previous_scores: List[float]) -> Dict:
        """
        Compare current score with user's interview history.
        Returns improvement/deterioration metrics.
        """
        if not previous_scores:
            return {"trend": "first", "improvement": 0.0, "avg_previous": 0.0}

        avg_previous = sum(previous_scores) / len(previous_scores)
        improvement = round(current_score - avg_previous, 1)

        if improvement > 5:
            trend = "improving"
        elif improvement < -5:
            trend = "declining"
        else:
            trend = "stable"

        return {
            "trend": trend,
            "improvement": improvement,
            "avg_previous": round(avg_previous, 1),
            "best_score": max(previous_scores + [current_score]),
            "total_interviews": len(previous_scores) + 1,
        }

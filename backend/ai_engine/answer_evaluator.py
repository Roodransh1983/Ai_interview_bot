"""
Answer Evaluator — scores user answers using TF-IDF cosine similarity
"""
from typing import Dict, List, Tuple
from ai_engine.nlp_processor import NLPProcessor
from ai_engine.confidence_detector import ConfidenceDetector


class AnswerEvaluator:
    """Evaluates interview answers using NLP similarity scoring"""

    def __init__(self):
        self.nlp = NLPProcessor()
        self.confidence = ConfidenceDetector()

    def evaluate(
        self,
        user_answer: str,
        ideal_answer: str,
        ideal_keywords: List[str],
        question_category: str,
    ) -> Dict:
        """
        Evaluate a user's answer against the ideal answer.

        Returns:
            Dict with:
                - score (0-100): Overall answer quality score
                - feedback: Text feedback for the user
                - keywords_matched: List of ideal keywords found in answer
                - keywords_missed: List of ideal keywords NOT found
                - confidence_score (0-100): Hesitation-based confidence
                - correct: Boolean if score >= 60
        """
        if not user_answer or not user_answer.strip():
            return {
                "score": 0.0,
                "feedback": "No answer provided. Please provide a response next time.",
                "keywords_matched": [],
                "keywords_missed": ideal_keywords,
                "confidence_score": 0.0,
                "correct": False,
            }

        # 1. Keyword match scoring (40% of total)
        matched_kw, missed_kw, keyword_score = self._score_keyword_match(
            user_answer, ideal_keywords
        )

        # 2. Semantic similarity scoring (40% of total)
        similarity_score = self.nlp.get_similarity(user_answer, ideal_answer) * 100

        # 3. Length adequacy scoring (20% of total)
        length_score = self._score_length(user_answer, ideal_answer)

        # Weighted total score
        total_score = round(
            keyword_score * 0.4 + similarity_score * 0.4 + length_score * 0.2, 1
        )

        # 4. Confidence detection
        confidence_score = self.confidence.detect(user_answer)

        # Generate feedback
        feedback = self._generate_feedback(
            total_score, matched_kw, missed_kw, similarity_score, keyword_score
        )

        return {
            "score": total_score,
            "feedback": feedback,
            "keywords_matched": matched_kw,
            "keywords_missed": missed_kw,
            "confidence_score": confidence_score,
            "correct": total_score >= 60,
        }

    def _score_keyword_match(
        self, user_answer: str, ideal_keywords: List[str]
    ) -> Tuple[List[str], List[str], float]:
        """Score based on how many ideal keywords appear in the answer"""
        user_keywords = set(k.lower() for k in self.nlp.extract_keywords(user_answer))
        ideal_set = set(k.lower() for k in ideal_keywords)

        matched = list(user_keywords.intersection(ideal_set))
        missed = list(ideal_set - user_keywords)

        if not ideal_set:
            return [], [], 50.0  # Neutral if no ideal keywords defined

        # Score: percentage of ideal keywords matched
        score = (len(matched) / len(ideal_set)) * 100
        return matched, missed, round(score, 2)

    def _score_length(self, user_answer: str, ideal_answer: str) -> float:
        """
        Score based on answer length adequacy.
        Penalize if too short or unreasonably long.
        Ideal is 50% to 150% of the ideal answer length.
        """
        user_len = len(user_answer.split())
        ideal_len = len(ideal_answer.split())

        if ideal_len == 0:
            return 50.0

        ratio = user_len / ideal_len

        if 0.5 <= ratio <= 1.5:
            return 100.0  # Ideal range
        elif ratio < 0.5:
            # Too short — linear penalty
            return max(0, (ratio / 0.5) * 100)
        else:
            # Too long — gradual penalty (being verbose is less bad than being terse)
            return max(0, 100 - (ratio - 1.5) * 20)

    def _generate_feedback(
        self,
        total_score: float,
        matched_kw: List[str],
        missed_kw: List[str],
        similarity: float,
        keyword_score: float,
    ) -> str:
        """Generate human-readable feedback based on scoring components"""
        if total_score >= 85:
            tone = "Excellent! "
        elif total_score >= 70:
            tone = "Good job! "
        elif total_score >= 50:
            tone = "Decent attempt, but "
        else:
            tone = "Needs improvement. "

        feedback_parts = [tone]

        if matched_kw:
            feedback_parts.append(
                f"You correctly covered: {', '.join(matched_kw[:5])}."
            )

        if missed_kw:
            feedback_parts.append(
                f"Consider mentioning: {', '.join(missed_kw[:3])}."
            )

        if similarity < 0.3 and matched_kw:
            feedback_parts.append(
                "Try to explain concepts in more detail with clearer examples."
            )
        elif similarity >= 0.7:
            feedback_parts.append("Your answer closely matches the expected response.")

        return " ".join(feedback_parts)

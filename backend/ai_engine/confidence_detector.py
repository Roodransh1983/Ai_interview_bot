"""
Confidence Detector — detects hesitation patterns in text answers
"""
import re
from typing import List


class ConfidenceDetector:
    """Detects confidence level from text using linguistic patterns"""

    # Hesitation and uncertainty words
    HESITATION_WORDS = {
        "um", "uh", "like", "maybe", "probably", "sort of", "kind of",
        "i think", "i guess", "i suppose", "i believe", "i feel",
        "not sure", "not certain", "not really", "pretty much",
        "somewhat", "rather", "quite", "fairly", "almost",
        "you know", "i mean", "well", "actually", "literally",
        "basically", "essentially", "totally", "definitely", "certainly",
    }

    # Confidence booster words
    BOOSTER_WORDS = {
        "definitely", "certainly", "absolutely", "clearly", "obviously",
        "always", "never", "must", "will", "can", "know", "understand",
        "expert", "proven", "achieved", "delivered", "led", "managed",
    }

    # Negative patterns that suggest low confidence
    UNCERTAINTY_PATTERNS = [
        r"\bi don't know\b",
        r"\bnot sure\b",
        r"\bno idea\b",
        r"\bcan't remember\b",
        r"\bsorry\b",
        r"\bapolog\w*",
    ]

    def detect(self, text: str) -> float:
        """
        Analyze text and return a confidence score from 0-100.
        Lower score = more hesitation/uncertainty detected.
        """
        if not text or not text.strip():
            return 0.0

        text_lower = text.lower()
        words = text_lower.split()
        word_count = len(words)

        if word_count == 0:
            return 0.0

        # Count hesitation indicators
        hesitation_count = 0
        booster_count = 0

        for word in self.HESITATION_WORDS:
            hesitation_count += text_lower.count(word)

        for word in self.BOOSTER_WORDS:
            booster_count += text_lower.count(word)

        # Check uncertainty patterns
        uncertainty_count = 0
        for pattern in self.UNCERTAINTY_PATTERNS:
            uncertainty_count += len(re.findall(pattern, text_lower))

        # Calculate base score
        # Each hesitation word adds penalty, each booster reduces it
        hesitation_ratio = hesitation_count / word_count
        booster_ratio = booster_count / word_count
        uncertainty_ratio = uncertainty_count / max(1, word_count / 10)  # Normalize

        # Score starts at 80 (assuming decent confidence), penalties bring it down
        score = 80.0
        score -= hesitation_ratio * 300  # Strong penalty for hesitation
        score += booster_ratio * 100      # Small boost for confidence words
        score -= uncertainty_ratio * 50   # Penalty for explicit uncertainty

        # Range clamp
        return max(0.0, min(100.0, round(score, 1)))

    def get_analysis(self, text: str) -> dict:
        """
        Get detailed confidence analysis.
        Returns breakdown of hesitation/booster words found.
        """
        if not text or not text.strip():
            return {"score": 0.0, "hesitation_words": [], "booster_words": []}

        text_lower = text.lower()

        hesitation_found = [w for w in self.HESITATION_WORDS if w in text_lower]
        booster_found = [w for w in self.BOOSTER_WORDS if w in text_lower]

        return {
            "score": self.detect(text),
            "hesitation_words": hesitation_found,
            "booster_words": booster_found,
            "total_hesitations": len(hesitation_found),
            "total_boosters": len(booster_found),
        }

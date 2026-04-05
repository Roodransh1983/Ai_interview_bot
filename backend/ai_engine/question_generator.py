"""
Question Generator — maps resume keywords to relevant questions from the question bank
"""
from typing import List, Dict
from ai_engine.question_bank import QuestionBank


# Mapping of skill keywords to question categories
SKILL_CATEGORY_MAP = {
    # Python
    "python": "Python",
    "django": "Python",
    "flask": "Python",
    "fastapi": "Python",
    "pandas": "Python",
    "numpy": "Python",
    # JavaScript
    "javascript": "JavaScript",
    "js": "JavaScript",
    "ecmascript": "JavaScript",
    "node": "Node.js",
    "nodejs": "Node.js",
    "express": "Node.js",
    "react": "React",
    "reactjs": "React",
    "vue": "React",
    "angular": "React",
    # Java
    "java": "Java",
    "spring": "Java",
    "springboot": "Java",
    "kotlin": "Java",
    # SQL & Database
    "sql": "SQL",
    "mysql": "SQL",
    "postgresql": "SQL",
    "mongodb": "SQL",
    "database": "SQL",
    # Machine Learning
    "machine learning": "Machine Learning",
    "ml": "Machine Learning",
    "deep learning": "Machine Learning",
    "tensorflow": "Machine Learning",
    "pytorch": "Machine Learning",
    "scikit-learn": "Machine Learning",
    "sklearn": "Machine Learning",
    "nlp": "Machine Learning",
    "neural network": "Machine Learning",
    # Data Structures
    "data structures": "Data Structures",
    "algorithm": "Data Structures",
    "arrays": "Data Structures",
    "linked list": "Data Structures",
    "tree": "Data Structures",
    "graph": "Data Structures",
    "hash": "Data Structures",
    "stack": "Data Structures",
    "queue": "Data Structures",
}


class QuestionGenerator:
    """Generates relevant interview questions based on resume keywords"""

    def __init__(self):
        self.bank = QuestionBank()
        self.skill_map = SKILL_CATEGORY_MAP

    def generate(
        self,
        resume_skills: List[str],
        num_questions: int = 5,
        difficulty: str = "medium",
        include_hr: bool = True,
    ) -> List[Dict]:
        """
        Generate an interview question sequence based on resume skills.

        Args:
            resume_skills: List of skill keywords extracted from resume
            num_questions: Total questions to generate
            difficulty: easy, medium, hard, or all
            include_hr: Whether to include HR/behavioral questions

        Returns:
            List of question dicts from the question bank
        """
        # Map resume skills to categories
        categories = self._map_skills_to_categories(resume_skills)

        # Always add HR questions
        if include_hr:
            categories.append("HR")

        # Remove duplicates
        categories = list(dict.fromkeys(categories))

        # Determine how many questions per category
        total_cats = len(categories)
        if total_cats == 0:
            # Fallback: use all categories
            categories = self.bank.get_all_categories()

        # Distribute questions across categories
        questions = []
        remaining = num_questions
        per_category = max(1, remaining // total_cats)

        for category in categories:
            cat_questions = self.bank.get_random_questions(
                [category], count=per_category, difficulty=difficulty
            )
            questions.extend(cat_questions)
            remaining -= len(cat_questions)

            if remaining <= 0:
                break

        # Fill remaining slots with random questions if needed
        if len(questions) < num_questions:
            all_random = self.bank.get_random_questions(
                self.bank.get_all_categories(),
                count=num_questions - len(questions),
                difficulty="all",
            )
            questions.extend(all_random)

        # Trim to exact count and shuffle for variety
        import random
        questions = questions[:num_questions]
        random.shuffle(questions)

        return questions

    def _map_skills_to_categories(self, skills: List[str]) -> List[str]:
        """Map a list of skills to their corresponding question categories"""
        categories = []
        for skill in skills:
            skill_lower = skill.lower().strip()
            if skill_lower in self.skill_map:
                categories.append(self.skill_map[skill_lower])
            else:
                # Try partial matching
                for key, value in self.skill_map.items():
                    if key in skill_lower or skill_lower in key:
                        if value not in categories:
                            categories.append(value)
                        break

        return categories

    def get_category_for_skill(self, skill: str) -> str:
        """Get the question category for a single skill"""
        skill_lower = skill.lower().strip()
        return self.skill_map.get(skill_lower, None)

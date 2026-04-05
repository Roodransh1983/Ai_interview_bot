"""
Resume parsing and keyword extraction service
"""
import os
import re
from typing import Dict, List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from PyPDF2 import PdfReader
from docx import Document
from app.config import settings
from app.models.user import ResumeData
from ai_engine.nlp_processor import NLPProcessor

nlp = NLPProcessor()

# Common skill keywords to look for
SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "c++", "c#", "ruby", "go", "rust", "typescript",
    "php", "swift", "kotlin", "scala", "r", "matlab", "perl", "haskell",
    # Frameworks & Libraries
    "react", "angular", "vue", "django", "flask", "fastapi", "spring", "springboot",
    "node.js", "express", "next.js", "gatsby", "redux", "tailwind", "bootstrap",
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "cassandra",
    "oracle", "sqlite", "dynamodb", "firebase",
    # Tools & Platforms
    "git", "docker", "kubernetes", "aws", "azure", "gcp", "linux", "jenkins",
    "terraform", "ansible", "nginx", "apache", "webpack",
    # Data Science / ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "nltk", "spacy", "opencv", "tableau", "powerbi",
    # Soft Skills / Other
    "leadership", "communication", "problem solving", "agile", "scrum",
]


class ResumeService:
    """Handles resume upload, parsing, and keyword extraction"""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users
        self.nlp = nlp

    async def upload_and_parse(
        self, user_id: str, file_path: str, file_extension: str
    ) -> ResumeData:
        """Upload and parse a resume file"""
        # Extract text based on file type
        if file_extension.lower() == ".pdf":
            text = self._extract_pdf(file_path)
        elif file_extension.lower() in [".docx", ".doc"]:
            text = self._extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")

        # Parse and extract structured data
        resume_data = self._parse_resume_text(text)

        # Store parsed data in user document
        await self.collection.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$set": {
                    "resume_uploaded": True,
                    "resume_data": resume_data.model_dump(),
                }
            },
        )

        return resume_data

    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            reader = PdfReader(file_path)
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n".join(text_parts)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return ""

    def _extract_docx(self, file_path: str) -> str:
        """Extract text from a DOCX file"""
        try:
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return ""

    def _parse_resume_text(self, text: str) -> ResumeData:
        """
        Parse resume text to extract skills, projects, and experience.
        Uses keyword matching and NLP extraction.
        """
        text_lower = text.lower()

        # Extract skills by matching against known keywords
        found_skills = []
        for skill in SKILL_KEYWORDS:
            if skill.lower() in text_lower:
                # Capitalize properly for display
                found_skills.append(skill.title() if skill.islower() else skill)

        # Also extract using NLP keyword extraction
        nlp_keywords = self.nlp.extract_keywords(text, top_n=20)
        for kw in nlp_keywords:
            if kw.title() not in found_skills and len(kw) > 2:
                found_skills.append(kw.title())

        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for s in found_skills:
            s_norm = s.lower()
            if s_norm not in seen:
                seen.add(s_norm)
                unique_skills.append(s)

        # Extract projects (look for section headers and following content)
        projects = self._extract_section(text, ["project", "portfolio", "work sample"])

        # Extract experience (look for section headers and following content)
        experience = self._extract_section(text, ["experience", "employment", "work history"])

        return ResumeData(
            skills=unique_skills[:30],  # Cap at 30 skills
            projects=projects[:10],      # Cap at 10 projects
            experience=experience[:5],   # Cap at 5 experience entries
            raw_text=text[:5000],        # Store first 5000 chars
        )

    def _extract_section(self, text: str, keywords: List[str]) -> List[str]:
        """
        Extract content sections based on header keywords.
        Looks for lines containing keywords and returns surrounding content.
        """
        lines = text.split("\n")
        sections = []
        current_section = []

        for line in lines:
            line_stripped = line.strip()
            # Check if line is a section header
            is_header = any(kw in line_stripped.lower() for kw in keywords)

            if is_header and current_section:
                # Save previous section
                section_text = " ".join(current_section)
                if len(section_text) > 20:  # Only save meaningful sections
                    sections.append(section_text[:200])  # Cap at 200 chars
                current_section = []
            elif line_stripped and not is_header:
                # Accumulate content under current section
                if len(line_stripped) > 3:  # Skip very short lines
                    current_section.append(line_stripped)

        return sections

    async def get_resume(self, user_id: str) -> ResumeData:
        """Get stored resume data for a user"""
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user or not user.get("resume_data"):
            return ResumeData()

        return ResumeData(**user["resume_data"])

from pydantic import BaseModel, Field
from typing import List, Optional


class ResumeInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    phone: str = Field(..., min_length=10)
    target_role: str = Field(..., min_length=2, max_length=100)
    experience_years: int = Field(..., ge=0, le=50)
    skills: List[str] = Field(..., min_length=1)
    education: str = Field(..., min_length=5)
    work_history: str = Field(..., min_length=10)


class GeneratedResume(BaseModel):
    content: str
    name: str
    email: str
    target_role: str
    format: str = "json"


class ATSInput(BaseModel):
    resume_text: str = Field(..., min_length=50, max_length=10000)
    job_description: str = Field(..., min_length=50, max_length=5000)


class ATSResult(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    keyword_score: float
    formatting_score: int
    formatting_issues: List[dict]
    missing_keywords: List[str] = []
    ai_feedback: str


class BulletImproveInput(BaseModel):
    bullet: str = Field(..., min_length=10, max_length=500)
    role: str = Field(..., min_length=2, max_length=100)

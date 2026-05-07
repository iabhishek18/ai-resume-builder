from pydantic import BaseModel
from typing import List, Optional

class ResumeInput(BaseModel):
    name: str
    email: str
    phone: str
    target_role: str
    experience_years: int
    skills: List[str]
    education: str
    work_history: str

class GeneratedResume(BaseModel):
    content: str
    name: str
    email: str
    target_role: str
    format: str = "json"

class ATSInput(BaseModel):
    resume_text: str
    job_description: str

class ATSResult(BaseModel):
    overall_score: int
    keyword_score: float
    formatting_score: int
    formatting_issues: List[str]
    ai_feedback: str

class BulletImproveInput(BaseModel):
    bullet: str
    role: str

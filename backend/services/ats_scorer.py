import openai
import os
import re
from models.resume import ATSResult

_api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=_api_key) if _api_key else None


def calculate_keyword_match(resume_text: str, job_description: str) -> float:
    jd_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", job_description.lower()))
    resume_words = set(re.findall(r"\b[a-zA-Z]{3,}\b", resume_text.lower()))
    common_words = {
        "the",
        "and",
        "for",
        "that",
        "with",
        "this",
        "from",
        "are",
        "was",
        "will",
        "have",
        "been",
    }
    jd_keywords = jd_words - common_words
    matched = jd_keywords.intersection(resume_words)
    return (len(matched) / max(len(jd_keywords), 1)) * 100


def check_formatting(resume_text: str) -> dict:
    issues = []
    if len(resume_text) < 200:
        issues.append("Resume appears too short")
    if len(resume_text) > 5000:
        issues.append("Resume may be too long for ATS")
    if not re.search(r"[\w\.-]+@[\w\.-]+\.\w+", resume_text):
        issues.append("No email address detected")
    if not re.search(r"\d{10}|\(\d{3}\)\s?\d{3}-\d{4}", resume_text):
        issues.append("No phone number detected")
    sections = ["experience", "education", "skills"]
    for section in sections:
        if section not in resume_text.lower():
            issues.append(f"Missing '{section}' section header")
    return {"issues": issues, "score": max(0, 100 - len(issues) * 15)}


async def score_resume(resume_text: str, job_description: str) -> ATSResult:
    keyword_score = calculate_keyword_match(resume_text, job_description)
    format_result = check_formatting(resume_text)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an ATS (Applicant Tracking System) expert. Analyze the resume against the job description.",
            },
            {
                "role": "user",
                "content": f"Resume:\n{resume_text}\n\nJob Description:\n{job_description}\n\nProvide: 1) Overall ATS score (0-100) 2) Missing keywords 3) Improvement suggestions",
            },
        ],
        temperature=0.3,
        max_tokens=1000,
    )

    ai_feedback = response.choices[0].message.content or ""
    overall_score = int((keyword_score + format_result["score"]) / 2)

    return ATSResult(
        overall_score=overall_score,
        keyword_score=round(keyword_score, 1),
        formatting_score=format_result["score"],
        formatting_issues=format_result["issues"],
        ai_feedback=ai_feedback,
    )

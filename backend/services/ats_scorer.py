import openai
import os
import re
from typing import Optional
from models.resume import ATSResult


def _get_client() -> Optional[openai.OpenAI]:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    return openai.OpenAI(api_key=key)


def calculate_keyword_match(resume_text: str, job_description: str) -> float:
    stop_words = {"the", "and", "for", "that", "with", "this", "from", "are", "was", "will", "have", "been", "been", "they", "their", "which", "about", "would", "make", "like", "just", "over", "such"}
    jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())) - stop_words
    resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower())) - stop_words

    if not jd_words:
        return 0.0

    matched = jd_words.intersection(resume_words)
    missing = jd_words - resume_words

    return round((len(matched) / len(jd_words)) * 100, 1)


def check_formatting(resume_text: str) -> dict:
    issues = []
    score = 100

    if len(resume_text) < 300:
        issues.append({"issue": "Resume too short", "severity": "high", "fix": "Add more content (aim for 400-800 words)"})
        score -= 20
    elif len(resume_text) > 5000:
        issues.append({"issue": "Resume too long", "severity": "medium", "fix": "Keep to 1-2 pages (under 1000 words)"})
        score -= 10

    if not re.search(r'[\w\.-]+@[\w\.-]+\.\w+', resume_text):
        issues.append({"issue": "No email address found", "severity": "high", "fix": "Add your email in contact section"})
        score -= 15

    if not re.search(r'\d{10}|\(\d{3}\)\s?\d{3}[-.]?\d{4}|\+\d{1,3}\s?\d{10}', resume_text):
        issues.append({"issue": "No phone number detected", "severity": "medium", "fix": "Add phone number"})
        score -= 10

    required_sections = ["experience", "education", "skills"]
    for section in required_sections:
        if section not in resume_text.lower():
            issues.append({"issue": f"Missing '{section}' section", "severity": "high", "fix": f"Add a clearly labeled '{section.title()}' section"})
            score -= 15

    if re.search(r'[■●►▪★]', resume_text):
        issues.append({"issue": "Special characters detected", "severity": "medium", "fix": "Use simple bullets (- or *) for ATS compatibility"})
        score -= 5

    return {"issues": issues, "score": max(0, score)}


async def score_resume(resume_text: str, job_description: str) -> ATSResult:
    keyword_score = calculate_keyword_match(resume_text, job_description)
    format_result = check_formatting(resume_text)

    missing_keywords = list(
        (set(re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())) -
         set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower())) -
         {"the", "and", "for", "that", "with", "this", "from"})
    )[:20]

    overall_score = int((keyword_score * 0.6) + (format_result["score"] * 0.4))

    ai_feedback = ""
    client = _get_client()
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an ATS expert. Provide 3-5 specific, actionable suggestions to improve this resume's ATS compatibility."},
                    {"role": "user", "content": f"Resume:\n{resume_text[:2000]}\n\nJob Description:\n{job_description[:1000]}"},
                ],
                temperature=0.3,
                max_tokens=500,
            )
            ai_feedback = response.choices[0].message.content or ""
        except Exception:
            ai_feedback = "AI feedback unavailable (check API key)"
    else:
        ai_feedback = "AI feedback requires OPENAI_API_KEY to be configured"

    return ATSResult(
        overall_score=overall_score,
        keyword_score=keyword_score,
        formatting_score=format_result["score"],
        formatting_issues=format_result["issues"],
        missing_keywords=missing_keywords[:15],
        ai_feedback=ai_feedback,
    )

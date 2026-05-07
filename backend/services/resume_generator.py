import openai
import os
from typing import Optional
from models.resume import ResumeInput, GeneratedResume


def _get_client() -> openai.OpenAI:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY environment variable is required. Set it in your .env file.")
    return openai.OpenAI(api_key=key)


async def generate_resume(input_data: ResumeInput) -> GeneratedResume:
    client = _get_client()

    system_prompt = (
        "You are a professional resume writer with 15 years of experience. "
        "Generate ATS-optimized resumes that pass automated screening systems. "
        "Use strong action verbs, quantify achievements, and follow the STAR method."
    )

    user_prompt = f"""Generate a professional resume with these details:
Name: {input_data.name}
Email: {input_data.email}
Phone: {input_data.phone}
Target Role: {input_data.target_role}
Experience: {input_data.experience_years} years
Skills: {', '.join(input_data.skills)}
Education: {input_data.education}
Work History: {input_data.work_history}

Return a JSON object with:
- summary: Professional summary (3-4 sentences)
- experience: Array of {{ company, role, duration, bullets: string[] }}
- skills_grouped: {{ technical: string[], soft: string[], tools: string[] }}
- education_formatted: string"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=2000,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    return GeneratedResume(
        content=content,
        name=input_data.name,
        email=input_data.email,
        target_role=input_data.target_role,
        format="json",
    )


async def improve_bullet_point(bullet: str, role: str) -> str:
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "Improve this resume bullet point using the STAR method. "
                    "Make it quantifiable, action-oriented, and ATS-friendly. "
                    "Start with a strong action verb. Include metrics where possible."
                ),
            },
            {"role": "user", "content": f"Role: {role}\nOriginal: {bullet}"},
        ],
        temperature=0.5,
        max_tokens=200,
    )
    return response.choices[0].message.content or bullet

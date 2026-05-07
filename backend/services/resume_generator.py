import openai
import os
from models.resume import ResumeInput, GeneratedResume

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_resume(input_data: ResumeInput) -> GeneratedResume:
    prompt = f"""Generate a professional resume with the following details:
    Name: {input_data.name}
    Email: {input_data.email}
    Phone: {input_data.phone}
    Role: {input_data.target_role}
    Experience: {input_data.experience_years} years
    Skills: {', '.join(input_data.skills)}
    Education: {input_data.education}
    Work History: {input_data.work_history}
    
    Generate a professional summary, bullet points for each role, and a skills section.
    Format as JSON with keys: summary, experience_bullets, skills_section, education_section"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional resume writer. Generate ATS-optimized resumes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2000
    )
    
    content = response.choices[0].message.content or ""
    return GeneratedResume(
        content=content,
        name=input_data.name,
        email=input_data.email,
        target_role=input_data.target_role,
        format="json"
    )

async def improve_bullet_point(bullet: str, role: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Improve this resume bullet point using STAR method. Make it quantifiable and action-oriented."},
            {"role": "user", "content": f"Role: {role}\nBullet: {bullet}"}
        ],
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].message.content or bullet

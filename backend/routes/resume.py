from fastapi import APIRouter
from models.resume import ResumeInput, BulletImproveInput
from services.resume_generator import generate_resume, improve_bullet_point

router = APIRouter()

@router.post("/generate")
async def generate(input_data: ResumeInput):
    result = await generate_resume(input_data)
    return {"success": True, "data": result}

@router.post("/improve-bullet")
async def improve_bullet(input_data: BulletImproveInput):
    improved = await improve_bullet_point(input_data.bullet, input_data.role)
    return {"success": True, "data": {"original": input_data.bullet, "improved": improved}}

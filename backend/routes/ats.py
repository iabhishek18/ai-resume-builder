from fastapi import APIRouter
from models.resume import ATSInput
from services.ats_scorer import score_resume

router = APIRouter()

@router.post("/score")
async def score(input_data: ATSInput):
    result = await score_resume(input_data.resume_text, input_data.job_description)
    return {"success": True, "data": result}

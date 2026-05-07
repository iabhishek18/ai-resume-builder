from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="AI Resume Builder API",
    version="2.0.0",
    description="GPT-4 powered resume generation and ATS scoring",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConfigError(Exception):
    def __init__(self, message: str):
        self.message = message


@app.exception_handler(ConfigError)
async def config_error_handler(_request: Request, exc: ConfigError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"success": False, "error": {"code": "CONFIG_ERROR", "message": exc.message}})


@app.exception_handler(Exception)
async def generic_error_handler(_request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content={"success": False, "error": {"code": "INTERNAL_ERROR", "message": str(exc)}})


from routes.resume import router as resume_router
from routes.ats import router as ats_router

app.include_router(resume_router, prefix="/api/resume", tags=["Resume"])
app.include_router(ats_router, prefix="/api/ats", tags=["ATS"])


@app.get("/health")
def health():
    has_key = bool(os.getenv("OPENAI_API_KEY"))
    return {
        "status": "ok",
        "openai_configured": has_key,
        "version": "2.0.0",
    }

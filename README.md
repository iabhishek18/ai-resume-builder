# AI Resume Builder with ATS Score Checker

AI-powered resume builder using GPT-4 for content generation and ATS compatibility scoring.

## Features

- 🤖 GPT-4 powered resume generation
- 📊 ATS (Applicant Tracking System) score checker
- 🎯 Keyword optimization against job descriptions
- ✏️ AI-powered bullet point improvement (STAR method)
- 📄 Multiple resume templates
- 📥 PDF export
- 💡 Real-time formatting suggestions

## Tech Stack

- **Backend**: Python, FastAPI, OpenAI GPT-4
- **Frontend**: React, Tailwind CSS
- **PDF Generation**: WeasyPrint + Jinja2

## Getting Started

```bash
git clone https://github.com/iabhishek18/ai-resume-builder.git
cd ai-resume-builder/backend
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI key
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/resume/generate | Generate resume from input |
| POST | /api/resume/improve-bullet | Improve a bullet point |
| POST | /api/ats/score | Score resume against JD |

## License

MIT

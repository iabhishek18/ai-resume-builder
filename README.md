# AI Resume Builder with ATS Score Checker

> Build ATS-optimized resumes with GPT-4 AI, get instant compatibility scores, and improve bullet points using the STAR method.

## 🚀 Overview

An AI-powered resume builder that leverages OpenAI's GPT-4 to generate professional, ATS-compatible resumes. The platform includes an intelligent ATS (Applicant Tracking System) scorer that analyzes your resume against specific job descriptions, identifies missing keywords, checks formatting issues, and provides actionable improvement suggestions.

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 GPT-4 Resume Generation | Generate complete professional resumes from basic input |
| 📊 ATS Score Checker | Score your resume against any job description (0-100) |
| 🎯 Keyword Analysis | Identify missing keywords from job postings |
| ✏️ Bullet Point Improver | Rewrite bullets using STAR method (Situation, Task, Action, Result) |
| 📐 Formatting Validator | Check for ATS-breaking formatting issues |
| 📄 Multiple Templates | Choose from professional resume layouts |
| 📥 PDF Export | Download formatted resumes as PDF |
| 💡 Real-time Suggestions | Live feedback as you edit |

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Backend | Python + FastAPI | Async REST API |
| AI | OpenAI GPT-4 | Content generation & analysis |
| PDF | WeasyPrint + Jinja2 | PDF rendering |
| Frontend | React + Tailwind | User interface |
| Validation | Pydantic | Request/response validation |

## 📁 Project Structure

```
ai-resume-builder/
├── backend/
│   ├── main.py                    # FastAPI app entry point
│   ├── requirements.txt           # Python dependencies
│   ├── services/
│   │   ├── resume_generator.py    # GPT-4 resume generation logic
│   │   └── ats_scorer.py          # ATS scoring algorithm
│   ├── routes/
│   │   ├── resume.py              # Resume generation endpoints
│   │   └── ats.py                 # ATS scoring endpoints
│   └── models/
│       └── resume.py              # Pydantic models
├── frontend/                      # React frontend
├── .env.example
└── .gitignore
```

## ⚡ Quick Start

### Prerequisites
- **Python** 3.11+
- **OpenAI API key** (GPT-4 access required)

### Installation

```bash
git clone https://github.com/iabhishek18/ai-resume-builder.git
cd ai-resume-builder/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env
# Add your OpenAI API key to .env

# Start the server
uvicorn main:app --reload --port 5000
```

API available at `http://localhost:5000` | Docs at `http://localhost:5000/docs`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key with GPT-4 access | Yes |

## 📡 API Reference

| Method | Endpoint | Description | Body |
|--------|----------|-------------|------|
| POST | `/api/resume/generate` | Generate full resume | `{name, email, phone, target_role, skills[], experience_years, education, work_history}` |
| POST | `/api/resume/improve-bullet` | Improve a bullet point | `{bullet, role}` |
| POST | `/api/ats/score` | Score resume vs job description | `{resume_text, job_description}` |
| GET | `/health` | Health check | - |

### Example: Generate Resume

```bash
curl -X POST http://localhost:5000/api/resume/generate \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","phone":"1234567890","target_role":"Senior Software Engineer","experience_years":5,"skills":["Python","React","AWS"],"education":"B.Tech CS - IIT Delhi","work_history":"2 years at Google, 3 years at startup"}'
```

### Example: ATS Score

```bash
curl -X POST http://localhost:5000/api/ats/score \
  -H "Content-Type: application/json" \
  -d '{"resume_text":"Your resume content here...","job_description":"We are looking for a Python developer with..."}'
```

## 🏗️ Architecture

```
Client → FastAPI → OpenAI GPT-4 API
                 → ATS Scoring Engine (keyword matching + formatting checks)
                 → PDF Generator (WeasyPrint)
```

## 📄 License

MIT

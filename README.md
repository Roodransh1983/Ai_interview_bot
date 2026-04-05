# AI Interview Bot

A complete, full-featured AI interview simulation platform built with a **custom AI engine** (no external AI APIs like OpenAI, Claude, or Ollama).

## Features

- 🔐 **Authentication** — JWT-based login/register with bcrypt password hashing
- 📄 **Resume Upload** — PDF/DOCX parsing with NLP keyword extraction
- 🤖 **Custom AI Engine** — TF-IDF cosine similarity, NLTK NLP, rule-based question generation
- 💬 **Text Interview Mode** — Real-time chat with AI interviewer
- 🎥 **Video Interview Mode** — WebRTC + MediaPipe face detection ("looking away" warning)
- 📊 **Scoring & Reports** — Per-question scores, radar charts, strengths/weaknesses
- 📧 **Email Reports** — HTML email reports via SMTP
- 🏆 **Leaderboard** — Ranked by average interview score
- 🎨 **Modern UI** — React + Tailwind + Framer Motion, dark/light mode

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, Tailwind CSS, Framer Motion, Recharts |
| State | Zustand |
| Backend | FastAPI, Python 3.11+ |
| AI | NLTK, spaCy, Scikit-learn (TF-IDF, cosine similarity) |
| Database | MongoDB + Motor (async) |
| Auth | JWT (PyJWT), bcrypt |
| Real-time | WebSocket (FastAPI) |
| Video | WebRTC, MediaPipe FaceMesh |

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB (local or Atlas)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your MongoDB URI and SMTP credentials

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"

# Run server
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run dev server
npm run dev
```

### Using Docker

```bash
docker-compose up
```

## Project Structure

```
ai-interview-bot/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry
│   │   ├── config.py            # Settings
│   │   ├── database.py          # MongoDB connection
│   │   ├── models/              # Pydantic models
│   │   ├── routes/              # API endpoints
│   │   └── services/            # Business logic
│   ├── ai_engine/               # Custom AI module
│   │   ├── question_bank.py     # Pre-defined questions
│   │   ├── question_generator.py
│   │   ├── nlp_processor.py     # TF-IDF, tokenization
│   │   ├── answer_evaluator.py  # Cosine similarity scoring
│   │   ├── confidence_detector.py
│   │   └── scoring_engine.py     # Report generation
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/               # Route pages
│   │   ├── components/          # Reusable components
│   │   ├── store/               # Zustand stores
│   │   └── services/            # API client
│   └── package.json
└── docker-compose.yml
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /auth/register | Register new user |
| POST | /auth/login | Login |
| GET | /auth/me | Get current user |
| POST | /resume/upload | Upload & parse resume |
| GET | /resume/ | Get parsed resume |
| POST | /interview/start | Start interview session |
| POST | /interview/answer | Submit answer |
| POST | /interview/complete/{id} | Complete & get report |
| WS | /interview/ws | Real-time interview |
| GET | /report/{id} | Get report |
| POST | /report/{id}/email | Send email report |
| GET | /leaderboard/ | Get leaderboard |

## How the AI Works

1. **Resume Parsing** — Extracts skills using PyPDF2/python-docx + NLTK keyword extraction
2. **Question Generation** — Maps resume skills to categorized question bank
3. **Answer Evaluation** — TF-IDF vectorization + cosine similarity against ideal answers
4. **Confidence Detection** — Hesitation word counting ("um", "maybe", etc.)
5. **Scoring** — Weighted average of keyword match (40%) + semantic similarity (40%) + length (20%)

## Deployment

- **Frontend**: Vercel (with API proxy to backend)
- **Backend**: Render, Railway, or any Python hosting
- **Database**: MongoDB Atlas (cloud) or self-hosted

See `.env.example` for required environment variables.

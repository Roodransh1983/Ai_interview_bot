"""
FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import connect_db, close_db
from app.routes import auth, resume, interview, report, leaderboard

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    await connect_db()
    yield
    await close_db()

app = FastAPI(
    title="AI Interview Bot API",
    description="Custom AI-powered interview simulation platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware — allow frontend to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(report.router)
app.include_router(leaderboard.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-interview-bot-api"}

@app.get("/")
async def root():
    return {"message": "AI Interview Bot API is running", "version": "1.0.0"}

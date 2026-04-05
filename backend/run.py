"""
Backend entry point for AI Interview Bot
Run with: uvicorn run:app --reload --port 8000
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

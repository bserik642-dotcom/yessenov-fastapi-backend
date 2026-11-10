from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import assistant, feedback
from app.config import ALLOWED_ORIGINS

app = FastAPI(
    title="Yessenov Campus Navigation Backend",
    description="FastAPI backend for AI Assistant and Student Feedback",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    return {"status": "ok", "service": "Yessenov Campus Navigation Backend"}

@app.get("/health")
def health():
    return {"status": "healthy"}

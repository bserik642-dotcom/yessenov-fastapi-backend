# Yessenov Campus Navigation - FastAPI Backend

FastAPI backend for Yessenov University Campus Navigation (AI Assistant & Student Feedback persistence).

## Features
- **AI Assistant API (`POST /v1/assistant`)**: Answers campus navigation questions in Kazakh, Russian, and English with Yessenov campus context.
- **Feedback API (`POST /v1/feedback`)**: Receives student feedback and persists it into the database.
- **Health Check (`GET /health`)**: For Render uptime and status monitoring.

## Project Structure
- `app/main.py`: FastAPI entrypoint, CORS configuration
- `app/config.py`: Environment variables & configuration
- `app/models.py`: Pydantic schemas (Assistant & Feedback)
- `app/routes/assistant.py`: AI Assistant endpoint
- `app/routes/feedback.py`: Feedback submission endpoint
- `requirements.txt`: Python dependencies
- `render.yaml`: Render blueprint deployment spec

## Environment Variables
- `INTERNAL_BACKEND_SECRET`: Secret token shared between website and backend
- `SUPABASE_URL`: Database URL
- `SUPABASE_SERVICE_ROLE_KEY`: Service key for inserting feedbacks
- `AI_API_KEY`: (Optional) OpenAI API key for LLM responses
- `ALLOWED_ORIGINS`: Comma-separated list of allowed web origins

## Deployment to Render
1. Open Render Dashboard and create a new Web Service.
2. Select repository `bserik642-dotcom/yessenov-fastapi-backend`.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables and click Deploy.

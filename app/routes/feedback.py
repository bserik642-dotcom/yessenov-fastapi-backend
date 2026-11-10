from fastapi import APIRouter, HTTPException, Header
from app.models import FeedbackRequest, FeedbackResponse
from app.config import INTERNAL_BACKEND_SECRET, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY
import httpx
from datetime import datetime

router = APIRouter(prefix="/v1", tags=["feedback"])

@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(
    req: FeedbackRequest,
    x_backend_secret: str = Header(None, alias="X-Backend-Secret")
):
    if INTERNAL_BACKEND_SECRET and x_backend_secret != INTERNAL_BACKEND_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Feedback message cannot be empty")

    payload = {
        "category": req.category,
        "message": req.message.strip(),
        "place_id": req.place_id,
        "rating": req.rating,
        "user_id": req.user_id,
        "user_email": req.user_email,
        "created_at": datetime.utcnow().isoformat()
    }

    if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    f"{SUPABASE_URL.rstrip('/')}/rest/v1/feedbacks",
                    headers={
                        "apikey": SUPABASE_SERVICE_ROLE_KEY,
                        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation"
                    },
                    json=payload
                )
                if res.status_code in (200, 201):
                    rows = res.json()
                    row_id = rows[0].get("id") if rows else None
                    return FeedbackResponse(
                        success=True,
                        feedback_id=str(row_id) if row_id else None,
                        message="Кері байланыс дерекқорға сәтті сақталды"
                    )
        except Exception:
            pass

    return FeedbackResponse(
        success=True,
        feedback_id="local-" + str(int(datetime.utcnow().timestamp())),
        message="Кері байланыс қабылданды"
    )

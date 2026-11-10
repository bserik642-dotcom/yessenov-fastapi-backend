from fastapi import APIRouter, HTTPException, Header
from app.models import AssistantRequest, AssistantResponse
from app.config import INTERNAL_BACKEND_SECRET, AI_API_KEY
import httpx

router = APIRouter(prefix="/v1", tags=["assistant"])

CAMPUS_CONTEXT = """
Yessenov University Campus Guide Context:
- Бас корпус (Main Building): 32-шағын аудан. Ректорат, дәріс залдары, негізгі деканаттар, кітапхана.
- 4-ші жатақхана (Dormitory 4): Студенттер үйі, асхана, оқу залы.
- 3-ші жатақхана (Dormitory 3): Студенттер үйі, демалыс аймағы.
- Технопарк (Technopark): IT-зертханалар, стартаптар, Decentrathon хакатоны өткен орын.
- Студенттік спорт кешені (Student Sports Complex): спорт залдары, жаттығу алаңдары.
- Қызмет көрсету орталығы (Service Center): студенттерге анықтамалар, құжаттар, ЦОС.
"""

@router.post("/assistant", response_model=AssistantResponse)
async def ask_assistant(
    req: AssistantRequest,
    x_backend_secret: str = Header(None, alias="X-Backend-Secret")
):
    if INTERNAL_BACKEND_SECRET and x_backend_secret != INTERNAL_BACKEND_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized request")

    user_query = req.message.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    system_prompt = f"""Сіз Yessenov University кампусының ресми AI көмекшісісіз.
Қазақша, орысша және ағылшынша сұрақтарға жауап бересіз.
Кампус ғимараттары, орындар және студенттерге қажетті қызметтер бойынша анық, сыпайы, пайдалы ақпарат беріңіз.

{CAMPUS_CONTEXT}
"""

    if AI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {AI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            *[{"role": m.role, "content": m.content} for m in (req.history or [])[-6:]],
                            {"role": "user", "content": user_query}
                        ],
                        "temperature": 0.4
                    }
                )
                if resp.status_code == 200:
                    data = resp.json()
                    reply = data["choices"][0]["message"]["content"]
                    return AssistantResponse(reply=reply)
        except Exception:
            pass

    reply = f"Сәлеметсіз бе! Yessenov University кампусы бойынша сұрағыңыз қабылданды: '{user_query}'. Бас корпус, 3 және 4-жатақханалар, Технопарк немесе Спорт кешені бойынша кез келген бағытты картадан таба аласыз."
    return AssistantResponse(reply=reply)

from pydantic import BaseModel, Field
from typing import Optional, List

class ChatMessage(BaseModel):
    role: str
    content: str

class AssistantRequest(BaseModel):
    message: str
    history: Optional[List[ChatMessage]] = Field(default_factory=list)
    language: Optional[str] = "kk"

class AssistantResponse(BaseModel):
    reply: str

class FeedbackRequest(BaseModel):
    category: str
    message: str
    place_id: Optional[str] = None
    rating: Optional[int] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    feedback_id: Optional[str] = None
    message: str

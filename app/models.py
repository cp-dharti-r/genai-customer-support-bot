from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    message: str = Field(..., description="User's message")
    provider: str = Field(..., description="LLM provider to use")
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")

class ChatResponse(BaseModel):
    response: str = Field(..., description="LLM response")
    provider: str = Field(..., description="LLM provider used")
    session_id: str = Field(..., description="Session ID")
    conversation_id: int = Field(..., description="Database conversation ID")
    timestamp: datetime = Field(..., description="Response timestamp")

class RatingRequest(BaseModel):
    conversation_id: int = Field(..., description="ID of conversation to rate")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback: Optional[str] = Field(None, description="Optional feedback text")

class RatingResponse(BaseModel):
    success: bool = Field(..., description="Whether rating was saved successfully")
    message: str = Field(..., description="Response message")

class ConversationHistory(BaseModel):
    id: int
    user_message: str
    llm_provider: str
    llm_response: str
    timestamp: datetime
    rating: Optional[int] = None
    feedback: Optional[str] = None

class AnalyticsResponse(BaseModel):
    daily_stats: dict = Field(..., description="Daily performance statistics")
    weekly_stats: dict = Field(..., description="Weekly performance statistics")
    provider_comparison: dict = Field(..., description="Provider performance comparison")

class FAQItem(BaseModel):
    id: int
    question: str
    answer: str
    category: str
    created_at: datetime

class ProviderInfo(BaseModel):
    name: str
    available: bool
    api_key_configured: bool

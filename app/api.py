from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid
from typing import List

from app.models import (
    ChatRequest, ChatResponse, RatingRequest, RatingResponse,
    ConversationHistory, AnalyticsResponse, FAQItem, ProviderInfo
)
from app.services import ChatService, RatingService, AnalyticsService, FAQService
from app.llm_providers import LLMProviderFactory
from app.database import create_tables
from app.config import settings

# Create FastAPI app
app = FastAPI(
    title="Customer Support Bot API",
    description="API for comparing different LLM providers in customer support scenarios",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
chat_service = ChatService()
rating_service = RatingService()
analytics_service = AnalyticsService()
faq_service = FAQService()

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_tables()

# API Routes
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message and return LLM response"""
    try:
        result = await chat_service.process_message(
            message=request.message,
            provider=request.provider,
            session_id=request.session_id
        )
        
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rate", response_model=RatingResponse)
async def rate_conversation(request: RatingRequest):
    """Rate a conversation response"""
    try:
        success = rating_service.save_rating(
            conversation_id=request.conversation_id,
            rating=request.rating,
            feedback=request.feedback
        )
        
        if success:
            return RatingResponse(success=True, message="Rating saved successfully")
        else:
            return RatingResponse(success=False, message="Failed to save rating")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics", response_model=AnalyticsResponse)
async def get_analytics():
    """Get daily and weekly analytics"""
    try:
        daily_stats = analytics_service.get_daily_stats()
        weekly_stats = analytics_service.get_weekly_stats()
        provider_comparison = analytics_service.get_provider_comparison()
        
        return AnalyticsResponse(
            daily_stats=daily_stats,
            weekly_stats=weekly_stats,
            provider_comparison=provider_comparison
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations", response_model=List[ConversationHistory])
async def get_conversation_history(session_id: str = None, limit: int = 50):
    """Get conversation history"""
    try:
        return analytics_service.get_conversation_history(session_id, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faqs", response_model=List[FAQItem])
async def get_faqs():
    """Get all FAQ items"""
    try:
        return faq_service.get_all_faqs()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/faqs/search", response_model=List[FAQItem])
async def search_faqs(query: str):
    """Search FAQs by query"""
    try:
        return faq_service.search_faqs(query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/providers", response_model=List[ProviderInfo])
async def get_providers():
    """Get available LLM providers and their status"""
    try:
        available_providers = LLMProviderFactory.get_available_providers()
        providers = []
        
        for provider_name in ["openai", "google"]:
            api_key_configured = False
            if provider_name == "openai" and settings.OPENAI_API_KEY:
                api_key_configured = True
            elif provider_name == "google" and settings.GOOGLE_API_KEY:
                api_key_configured = True
            
            providers.append(ProviderInfo(
                name=provider_name,
                available=provider_name in available_providers,
                api_key_configured=api_key_configured
            ))
        
        return providers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

# Serve static files and HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

# Root endpoint - redirect to chat interface
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main chat interface"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

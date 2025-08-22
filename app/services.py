import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from app.database import get_db, Conversation, Rating, FAQ
from app.llm_providers import LLMProviderFactory
from app.models import ConversationHistory, AnalyticsResponse

class ChatService:
    """Service for handling chat interactions"""
    
    def __init__(self):
        self.factory = LLMProviderFactory()
    
    async def process_message(self, message: str, provider: str, session_id: str = None) -> Dict[str, Any]:
        """Process a user message and return LLM response"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        try:
            # Create LLM provider
            llm_provider = self.factory.create_provider(provider)
            
            # Get FAQ context for better responses
            context = self._get_faq_context(message)
            
            # Generate response
            response = await llm_provider.generate_response(message, context)
            
            # Save conversation to database
            conversation_id = self._save_conversation(session_id, message, provider, response)
            
            return {
                "response": response,
                "provider": provider,
                "session_id": session_id,
                "conversation_id": conversation_id,
                "timestamp": datetime.utcnow()
            }
            
        except Exception as e:
            return {
                "response": f"Sorry, I encountered an error: {str(e)}",
                "provider": provider,
                "session_id": session_id,
                "conversation_id": None,
                "timestamp": datetime.utcnow()
            }
    
    def _get_faq_context(self, message: str) -> str:
        """Get relevant FAQ context for the message"""
        # This is a simplified version - in production you might use semantic search
        db = next(get_db())
        try:
            # Get recent FAQs for context
            faqs = db.query(FAQ).order_by(desc(FAQ.created_at)).limit(5).all()
            context = "\n".join([f"Q: {faq.question}\nA: {faq.answer}" for faq in faqs])
            return context
        finally:
            db.close()
    
    def _save_conversation(self, session_id: str, message: str, provider: str, response: str) -> int:
        """Save conversation to database"""
        db = next(get_db())
        try:
            conversation = Conversation(
                session_id=session_id,
                user_message=message,
                llm_provider=provider,
                llm_response=response
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            return conversation.id
        finally:
            db.close()

class RatingService:
    """Service for handling conversation ratings"""
    
    def save_rating(self, conversation_id: int, rating: int, feedback: str = None) -> bool:
        """Save a rating for a conversation"""
        db = next(get_db())
        try:
            # Check if conversation exists
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if not conversation:
                return False
            
            # Check if rating already exists
            existing_rating = db.query(Rating).filter(Rating.conversation_id == conversation_id).first()
            if existing_rating:
                # Update existing rating
                existing_rating.rating = rating
                existing_rating.feedback = feedback
                existing_rating.timestamp = datetime.utcnow()
            else:
                # Create new rating
                new_rating = Rating(
                    conversation_id=conversation_id,
                    rating=rating,
                    feedback=feedback
                )
                db.add(new_rating)
            
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            return False
        finally:
            db.close()

class AnalyticsService:
    """Service for generating analytics and performance metrics"""
    
    def get_daily_stats(self) -> Dict[str, Any]:
        """Get daily performance statistics"""
        db = next(get_db())
        try:
            today = datetime.utcnow().date()
            
            # Daily conversation count
            daily_conversations = db.query(Conversation).filter(
                func.date(Conversation.timestamp) == today
            ).count()
            
            # Daily average rating
            daily_ratings = db.query(func.avg(Rating.rating)).join(Conversation).filter(
                func.date(Conversation.timestamp) == today
            ).scalar() or 0
            
            return {
                "date": today.isoformat(),
                "total_conversations": daily_conversations,
                "average_rating": round(float(daily_ratings), 2),
                "total_ratings": db.query(Rating).join(Conversation).filter(
                    func.date(Conversation.timestamp) == today
                ).count()
            }
        finally:
            db.close()
    
    def get_weekly_stats(self) -> Dict[str, Any]:
        """Get weekly performance statistics"""
        db = next(get_db())
        try:
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            # Weekly conversation count
            weekly_conversations = db.query(Conversation).filter(
                Conversation.timestamp >= week_ago
            ).count()
            
            # Weekly average rating
            weekly_ratings = db.query(func.avg(Rating.rating)).join(Conversation).filter(
                Conversation.timestamp >= week_ago
            ).scalar() or 0
            
            return {
                "period": f"Last 7 days",
                "total_conversations": weekly_conversations,
                "average_rating": round(float(weekly_ratings), 2),
                "total_ratings": db.query(Rating).join(Conversation).filter(
                    Conversation.timestamp >= week_ago
                ).count()
            }
        finally:
            db.close()
    
    def get_provider_comparison(self) -> Dict[str, Any]:
        """Compare performance across different LLM providers"""
        db = next(get_db())
        try:
            providers = db.query(Conversation.llm_provider).distinct().all()
            comparison = {}
            
            for (provider,) in providers:
                # Get provider stats
                total_conversations = db.query(Conversation).filter(
                    Conversation.llm_provider == provider
                ).count()
                
                # Get average rating for provider
                avg_rating = db.query(func.avg(Rating.rating)).join(Conversation).filter(
                    Conversation.llm_provider == provider
                ).scalar() or 0
                
                comparison[provider] = {
                    "total_conversations": total_conversations,
                    "average_rating": round(float(avg_rating), 2),
                    "total_ratings": db.query(Rating).join(Conversation).filter(
                        Conversation.llm_provider == provider
                    ).count()
                }
            
            return comparison
        finally:
            db.close()
    
    def get_conversation_history(self, session_id: str = None, limit: int = 50) -> List[ConversationHistory]:
        """Get conversation history"""
        db = next(get_db())
        try:
            query = db.query(Conversation).outerjoin(Rating)
            
            if session_id:
                query = query.filter(Conversation.session_id == session_id)
            
            conversations = query.order_by(desc(Conversation.timestamp)).limit(limit).all()
            
            history = []
            for conv in conversations:
                rating = conv.rating.rating if conv.rating else None
                feedback = conv.rating.feedback if conv.rating else None
                
                history.append(ConversationHistory(
                    id=conv.id,
                    user_message=conv.user_message,
                    llm_provider=conv.llm_provider,
                    llm_response=conv.llm_response,
                    timestamp=conv.timestamp,
                    rating=rating,
                    feedback=feedback
                ))
            
            return history
        finally:
            db.close()

class FAQService:
    """Service for managing FAQ data"""
    
    def get_all_faqs(self) -> List[FAQ]:
        """Get all FAQ items"""
        db = next(get_db())
        try:
            return db.query(FAQ).order_by(FAQ.category, FAQ.created_at).all()
        finally:
            db.close()
    
    def search_faqs(self, query: str) -> List[FAQ]:
        """Search FAQs by query"""
        db = next(get_db())
        try:
            return db.query(FAQ).filter(
                FAQ.question.contains(query) | FAQ.answer.contains(query)
            ).all()
        finally:
            db.close()

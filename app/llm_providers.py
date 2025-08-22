import openai
import google.generativeai as genai
from typing import Dict, Any, Optional
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMProvider:
    """Base class for LLM providers"""
    
    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        self.client = None
        self._setup_client()
    
    def _setup_client(self):
        """Setup the client for the specific provider"""
        raise NotImplementedError
    
    async def generate_response(self, message: str, context: str = "") -> str:
        """Generate response from the LLM"""
        raise NotImplementedError

class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider"""
    
    def _setup_client(self):
        if not settings.OPENAI_API_KEY:
            raise ValueError("OpenAI API key not configured")
        openai.api_key = settings.OPENAI_API_KEY
        self.client = openai
    
    async def generate_response(self, message: str, context: str = "") -> str:
        try:
            system_prompt = f"""You are a helpful customer support agent for an e-commerce website. 
            Answer customer questions professionally and accurately. 
            If you don't know something, say so rather than making up information.
            
            Context: {context}
            
            Customer Question: {message}"""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=settings.MAX_TOKENS,
                temperature=settings.TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

class GoogleProvider(LLMProvider):
    """Google Gemini provider"""
    
    def _setup_client(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("Google API key not configured")
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.client = genai.GenerativeModel('gemini-2.5-flash-lite')
    
    async def generate_response(self, message: str, context: str = "") -> str:
        try:
            system_prompt = f"""You are a helpful customer support agent for an e-commerce website. 
            Answer customer questions professionally and accurately. 
            If you don't know something, say so rather than making up information.
            
            Context: {context}
            
            Customer Question: {message}"""
            
            response = self.client.generate_content(system_prompt + "\n\n" + message)
            return response.text
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            return f"Sorry, I encountered an error: {str(e)}"

class LLMProviderFactory:
    """Factory class to create LLM providers"""
    
    @staticmethod
    def create_provider(provider_name: str) -> LLMProvider:
        """Create and return an LLM provider instance"""
        providers = {
            "openai": OpenAIProvider,
            "google": GoogleProvider
        }
        
        if provider_name not in providers:
            raise ValueError(f"Unknown provider: {provider_name}")
        
        return providers[provider_name](provider_name)
    
    @staticmethod
    def get_available_providers() -> list:
        """Get list of available providers based on configured API keys"""
        available = []
        if settings.OPENAI_API_KEY:
            available.append("openai")
        if settings.GOOGLE_API_KEY:
            available.append("google")
        return available

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    # LLM API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./customer_support_bot.db")
    
    # LLM Configuration
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "openai")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1000"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    
    # Available LLM Providers (only OpenAI and Google)
    AVAILABLE_PROVIDERS = ["openai", "google"]
    
    def validate_api_keys(self):
        """Validate that at least one API key is provided"""
        if not any([self.OPENAI_API_KEY, self.GOOGLE_API_KEY]):
            raise ValueError("At least one LLM API key must be provided")

settings = Settings()

#!/usr/bin/env python3
"""
Customer Support Bot - LLM Comparison Tool
Main application entry point
"""

import uvicorn
from app.api import app
from app.config import settings
from app.database import create_tables
from app.seed_data import seed_faq_data

def main():
    """Main application function"""
    print("🚀 Starting Customer Support Bot...")
    
    # Create database tables
    print("📊 Setting up database...")
    create_tables()
    
    # Seed FAQ data
    print("🌱 Seeding FAQ data...")
    seed_faq_data()
    
    # Start the server
    print(f"🌐 Starting server on {settings.HOST}:{settings.PORT}")
    print("📖 API documentation available at: http://localhost:8000/docs")
    print("💬 Chat interface available at: http://localhost:8000/")
    
    uvicorn.run(
        "app.api:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )

if __name__ == "__main__":
    main()

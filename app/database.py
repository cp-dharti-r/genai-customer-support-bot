from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from app.config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text)
    llm_provider = Column(String, index=True)
    llm_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    rating = relationship("Rating", back_populates="conversation", uselist=False)

class Rating(Base):
    __tablename__ = "ratings"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    rating = Column(Integer)  # 1-5 scale
    feedback = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship("Conversation", back_populates="rating")

class FAQ(Base):
    __tablename__ = "faqs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    category = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

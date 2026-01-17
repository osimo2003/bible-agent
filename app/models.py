from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    language = Column(String, default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())
    
    # Bible study progress
    current_book = Column(String, default="Matthew")
    last_chapter = Column(Integer, default=0)
    total_days_engaged = Column(Integer, default=0)
    current_streak = Column(Integer, default=0)
    preferred_time = Column(String, default="08:00")
    
    # Preferences
    receive_daily_reminders = Column(Boolean, default=True)
    receive_checkins = Column(Boolean, default=True)
    study_style = Column(String, default="devotional")  # devotional, study, reflective

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    date = Column(DateTime(timezone=True), server_default=func.now())
    book = Column(String)
    chapter_start = Column(Integer)
    chapter_end = Column(Integer)
    completed = Column(Boolean, default=False)
    reading_time_minutes = Column(Integer, nullable=True)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book = Column(String)
    chapter = Column(Integer)
    verse = Column(String)  # Could be "1-3" or "5"
    note = Column(Text, nullable=True)
    tags = Column(JSON, default=[])  # ["encouragement", "peace", etc.]
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message_type = Column(String)  # "user_message", "agent_response"
    content = Column(Text)
    intent = Column(String, nullable=True)  # "daily_study", "verse_request", "prayer", etc.
    metadata = Column(JSON, nullable=True)  # {"verse": "John 3:16", "mood": "anxious"}
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    conversation_id = Column(Integer, nullable=True)
    rating = Column(Integer)  # 1-5
    feedback_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserBase(BaseModel):
    phone_number: str
    name: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    current_book: str
    last_chapter: int
    total_days_engaged: int
    current_streak: int
    
    class Config:
        from_attributes = True

# Message Schemas
class WhatsAppMessage(BaseModel):
    From: str
    Body: str
    
class AgentResponse(BaseModel):
    message: str
    options: Optional[List[str]] = None
    verse_reference: Optional[str] = None
    next_action: Optional[str] = None

# Bible Study Schemas
class DailyReading(BaseModel):
    book: str
    chapter_start: int
    chapter_end: int
    day_number: int
    total_days: int
    reflection_question: Optional[str] = None

class VerseRequest(BaseModel):
    topic: str
    mood: Optional[str] = None
    context: Optional[str] = None

# Feedback Schema
class FeedbackCreate(BaseModel):
    rating: int
    feedback_text: Optional[str] = None

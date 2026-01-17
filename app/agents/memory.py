from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from app import models, schemas

class MemoryAgent:
    def __init__(self, db: Session):
        self.db = db
    
    def get_or_create_user(self, phone_number: str) -> models.User:
        """Get user by phone number or create if not exists"""
        user = self.db.query(models.User).filter(
            models.User.phone_number == phone_number
        ).first()
        
        if not user:
            user = models.User(
                phone_number=phone_number,
                current_book="Matthew",
                last_chapter=0,
                total_days_engaged=0,
                current_streak=0
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        
        return user
    
    def update_user_progress(self, user_id: int, book: str, chapter_start: int, chapter_end: int) -> models.UserProgress:
        """Record user's daily reading progress"""
        progress = models.UserProgress(
            user_id=user_id,
            book=book,
            chapter_start=chapter_start,
            chapter_end=chapter_end,
            completed=True,
            reading_time_minutes=10
        )
        self.db.add(progress)
        
        
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.last_chapter = chapter_end
            user.current_book = book
            user.total_days_engaged += 1
            
            
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            
            
            yesterday_progress = self.db.query(models.UserProgress).filter(
                models.UserProgress.user_id == user_id,
                models.UserProgress.date >= yesterday,
                models.UserProgress.date < today
            ).first()
            
            if yesterday_progress:
                user.current_streak += 1
            else:
                user.current_streak = 1
        
        self.db.commit()
        return progress
    
    def add_bookmark(self, user_id: int, verse_ref: str, note: Optional[str] = None) -> models.Bookmark:
        """Save a verse as bookmark"""
        
        import re
        match = re.match(r'([1-3]?\s?[A-Za-z]+)\s+(\d+):(\d+)', verse_ref)
        
        bookmark = models.Bookmark(
            user_id=user_id,
            book=match.group(1).title() if match else "Unknown",
            chapter=int(match.group(2)) if match else 0,
            verse=match.group(3) if match else "0",
            note=note,
            tags=[]
        )
        self.db.add(bookmark)
        self.db.commit()
        self.db.refresh(bookmark)
        return bookmark
    
    def get_user_bookmarks(self, user_id: int) -> List[models.Bookmark]:
        """Get all bookmarks for a user"""
        return self.db.query(models.Bookmark).filter(
            models.Bookmark.user_id == user_id
        ).order_by(models.Bookmark.created_at.desc()).all()
    
    def get_user_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user statistics"""
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return {}
        
        
        total_nt_chapters = 260 
        chapters_read = self._calculate_chapters_read(user_id)
        
        return {
            "current_book": user.current_book,
            "last_chapter": user.last_chapter,
            "total_days_engaged": user.total_days_engaged,
            "current_streak": user.current_streak,
            "chapters_read": chapters_read,
            "completion_percentage": round((chapters_read / total_nt_chapters) * 100, 1),
            "total_bookmarks": self.db.query(models.Bookmark).filter(
                models.Bookmark.user_id == user_id
            ).count()
        }
    
    def _calculate_chapters_read(self, user_id: int) -> int:
        """Calculate total chapters read by user"""
        progress_entries = self.db.query(models.UserProgress).filter(
            models.UserProgress.user_id == user_id
        ).all()
        
        total = 0
        for entry in progress_entries:
            total += (entry.chapter_end - entry.chapter_start + 1)
        
        return total
    
    def save_conversation(self, user_id: int, message_type: str, content: str, 
                         intent: Optional[str] = None, metadata: Optional[Dict] = None):
        """Save conversation history"""
        conversation = models.Conversation(
            user_id=user_id,
            message_type=message_type,
            content=content,
            intent=intent,
            message_metadata=metadata or {}
        )
        self.db.add(conversation)
        self.db.commit()
    
    def save_feedback(self, user_id: int, rating: int, feedback_text: Optional[str] = None):
        """Save user feedback"""
        feedback = models.Feedback(
            user_id=user_id,
            rating=rating,
            feedback_text=feedback_text
        )
        self.db.add(feedback)
        self.db.commit()

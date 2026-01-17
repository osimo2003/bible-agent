from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, time
import logging
from typing import Dict, Any
from sqlalchemy.orm import Session

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

class SchedulerAgent:
    def __init__(self, db: Session):
        self.scheduler = BackgroundScheduler()
        self.db = db
        self.setup_schedules()
    
    def setup_schedules(self):
        """Setup all scheduled tasks"""
        # Morning reminder (8 AM)
        self.scheduler.add_job(
            self.send_morning_reminders,
            CronTrigger(hour=8, minute=0),
            id='morning_reminder',
            name='Send morning Bible study reminders'
        )
        
        # Evening check-in (8 PM)
        self.scheduler.add_job(
            self.send_evening_checkins,
            CronTrigger(hour=20, minute=0),
            id='evening_checkin',
            name='Send evening check-in messages'
        )
        
        # Weekly progress report (Sunday 9 AM)
        self.scheduler.add_job(
            self.send_weekly_reports,
            CronTrigger(day_of_week='sun', hour=9, minute=0),
            id='weekly_report',
            name='Send weekly progress reports'
        )
    
    def send_morning_reminders(self):
        """Send morning reminders to all users"""
        from app.agents.planner import PlannerAgent
        from app.agents.bible_matcher import BibleMatchingAgent
        from app.agents.response_composer import ResponseComposerAgent
        
        # Get all users who want reminders
        users = self.db.query(models.User).filter(
            models.User.receive_daily_reminders == True
        ).all()
        
        planner = PlannerAgent()
        bible_matcher = BibleMatchingAgent()
        composer = ResponseComposerAgent()
        
        for user in users:
            try:
                # Get today's reading
                reading_data = bible_matcher.get_daily_reading(
                    user.current_book, 
                    user.last_chapter
                )
                
                # Generate reflection question
                reading_data['reflection_question'] = bible_matcher.generate_reflection_question(
                    reading_data['book'], 
                    reading_data['chapter_start']
                )
                
                # Get user stats
                memory_agent = MemoryAgent(self.db)
                stats = memory_agent.get_user_stats(user.id)
                
                # Compose message
                message = composer.compose_daily_reading_response(reading_data, stats)
                
                # Send message (implement WhatsApp sending)
                self.send_whatsapp_message(user.phone_number, message)
                
                # Log the reminder
                memory_agent.save_conversation(
                    user.id,
                    "system_reminder",
                    f"Morning reminder sent: {reading_data['book']} {reading_data['chapter_start']}-{reading_data['chapter_end']}",
                    "daily_reminder"
                )
                
            except Exception as e:
                print(f"Error sending reminder to {user.phone_number}: {e}")
    
    def send_evening_checkins(self):
        """Send evening check-in messages"""
        # Implementation similar to morning reminders
        pass
    
    def send_weekly_reports(self):
        """Send weekly progress reports"""
        pass
    
    def send_whatsapp_message(self, phone_number: str, message: str):
        """Send WhatsApp message (to be implemented with Twilio)"""
        # This will be implemented in the WhatsApp routes
        print(f"[SCHEDULED] To {phone_number}: {message[:50]}...")
    
    def start(self):
        """Start the scheduler"""
        self.scheduler.start()
        print("Scheduler started")
    
    def shutdown(self):
        """Shutdown the scheduler"""
        self.scheduler.shutdown()
        print("Scheduler stopped")

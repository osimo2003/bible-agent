from typing import List, Dict, Any, Optional
from datetime import datetime
import random

class ResponseComposerAgent:
    def __init__(self):
        self.greetings = [
            "Peace be with you! 🙏",
            "Hello! Blessed to connect with you today. ✨",
            "Greetings in Jesus' name! ❤️",
            "Welcome back! Ready for God's word? 📖"
        ]
        
        self.closings = [
            "God bless you!",
            "Praying for you today.",
            "May God's peace be with you.",
            "Talk to you soon!"
        ]
    
    def compose_daily_reading_response(self, reading_data: Dict[str, Any], 
                                      user_stats: Dict[str, Any]) -> str:
        """Compose response for daily reading"""
        book = reading_data["book"]
        chapter_start = reading_data["chapter_start"]
        chapter_end = reading_data["chapter_end"]
        day_number = user_stats.get("total_days_engaged", 0) + 1
        
        response = f"""📖 *DAILY BIBLE STUDY* (Day {day_number})

Today's Reading:
*{book} {chapter_start}-{chapter_end}*

💡 Reflection Question:
{reading_data.get('reflection_question', 'What is God saying to you through this passage?')}

⏰ Take 10-15 minutes to read and reflect.

Reply READ when you're done.
Reply SKIP if today's not good.

---
📊 Your Progress: {user_stats.get('completion_percentage', 0)}% complete
🔥 Current streak: {user_stats.get('current_streak', 0)} days
"""
        
        if reading_data.get("is_new_book"):
            response += f"\n🎉 *New Book Alert:* Starting {book} today!"
        
        return response
    
    def compose_verse_response(self, verses: List[Dict[str, Any]], topic: str) -> str:
        """Compose response with verses for a topic"""
        if not verses:
            return self._compose_fallback_response(topic)
        
        response = f"📖 *Scripture for {topic.title()}*\n\n"
        
        for i, verse in enumerate(verses, 1):
            response += f"{i}. *{verse['book']} {verse['chapter']}:{verse['verse']}*\n"
            response += f"_{verse['text']}_\n\n"
        
        response += "💭 *Reflection:* How does this speak to your situation?\n\n"
        response += "💬 Reply with your thoughts, or type MENU for options."
        
        return response
    
    def compose_greeting(self) -> str:
        """Compose greeting message"""
        greeting = random.choice(self.greetings)
        return f"""{greeting}

I'm your Bible Study Companion! 🤖

Here's what I can help with:
📖 *DAILY* - Get today's Bible reading (2 chapters)
💬 *VERSE [topic]* - Get verses for any situation
🔖 *SAVE [verse]* - Bookmark a verse
📊 *PROGRESS* - Check your reading stats
🙏 *PRAYER* - Share a prayer request
❓ *HELP* - See all commands

What would you like to do?"""
    
    def compose_progress_response(self, stats: Dict[str, Any]) -> str:
        """Compose progress report"""
        return f"""📊 *YOUR BIBLE STUDY PROGRESS*

📚 Current Book: {stats.get('current_book', 'Matthew')} {stats.get('last_chapter', 0)}
📈 Completion: {stats.get('completion_percentage', 0)}% of New Testament
🔥 Current Streak: {stats.get('current_streak', 0)} days
📖 Total Days: {stats.get('total_days_engaged', 0)} days
🔖 Bookmarks: {stats.get('total_bookmarks', 0)} saved verses

💪 Keep going! Every chapter brings you closer to God.

Type DAILY to continue your journey!"""
    
    def compose_bookmark_saved(self, verse_ref: str) -> str:
        """Compose bookmark confirmation"""
        return f"""✅ *BOOKMARK SAVED*

"{verse_ref}" has been saved to your collection!

To view all bookmarks, type BOOKMARKS.

Keep treasuring God's Word in your heart! 💖"""
    
    def _compose_fallback_response(self, topic: str) -> str:
        """Compose response when no verses found"""
        fallbacks = {
            "anxiety": "Cast all your anxiety on him because he cares for you. (1 Peter 5:7)",
            "fear": "For God has not given us a spirit of fear, but of power and of love and of a sound mind. (2 Timothy 1:7)",
            "encouragement": "The LORD himself goes before you and will be with you; he will never leave you nor forsake you. Do not be afraid; do not be discouraged. (Deuteronomy 31:8)"
        }
        
        verse = fallbacks.get(topic, "Trust in the LORD with all your heart and lean not on your own understanding. (Proverbs 3:5)")
        
        return f"""📖 *Encouragement for You*

{verse}

💬 Want specific verses? Try: "verse about [topic]"
📖 Or continue daily reading with: DAILY"""
    
    def add_closing(self, response: str) -> str:
        """Add closing to response"""
        closing = random.choice(self.closings)
        return f"{response}\n\n— {closing}"

import re
from typing import Dict, Any, Optional
from app.schemas import WhatsAppMessage, AgentResponse

class PlannerAgent:
    def __init__(self):
        self.intent_keywords = {
            "daily_study": ["read", "study", "today", "chapter", "continue", "next"],
            "verse_request": ["verse", "scripture", "bible", "about", "help with", "feeling"],
            "prayer": ["pray", "prayer", "pray for"],
            "bookmark": ["save", "bookmark", "remember", "favorite"],
            "progress": ["progress", "how am i doing", "stats", "streak"],
            "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
            "help": ["help", "what can you do", "commands", "menu"]
        }
    
    def analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user message and determine intent"""
        message_lower = message.lower()
        
        # Check for specific patterns
        if self._is_daily_checkin(message_lower):
            return {"intent": "daily_checkin", "action": "mark_complete"}
        
        if self._is_bookmark_request(message_lower):
            verse_ref = self._extract_verse_reference(message)
            if verse_ref:
                return {"intent": "bookmark", "verse": verse_ref, "action": "save"}
        
        # Check keyword matches
        for intent, keywords in self.intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                # Special handling for verse requests
                if intent == "verse_request":
                    topic = self._extract_topic(message_lower)
                    return {
                        "intent": "verse_request",
                        "topic": topic,
                        "mood": self._detect_mood(message_lower)
                    }
                return {"intent": intent}
        
        # Default to conversation
        return {"intent": "conversation", "action": "respond_generally"}
    
    def _is_daily_checkin(self, message: str) -> bool:
        """Check if user is responding to daily reading"""
        checkin_words = ["done", "finished", "read", "completed", "✓", "check"]
        return any(word in message for word in checkin_words) and len(message.split()) < 5
    
    def _is_bookmark_request(self, message: str) -> bool:
        bookmark_words = ["save", "bookmark", "remember this", "favorite"]
        return any(word in message.lower() for word in bookmark_words)
    
    def _extract_verse_reference(self, message: str) -> Optional[str]:
        """Extract Bible verse reference from message"""
        pattern = r'([1-3]?\s?[A-Za-z]+)\s*(\d+):(\d+(-\d+)?)'
        match = re.search(pattern, message)
        if match:
            book = match.group(1).title()
            chapter = match.group(2)
            verse = match.group(3)
            return f"{book} {chapter}:{verse}"
        return None
    
    def _extract_topic(self, message: str) -> str:
        """Extract main topic from message"""
        # Remove common words
        stop_words = ["i'm", "i am", "feeling", "about", "my", "me", "please", "can you"]
        words = message.lower().split()
        filtered = [w for w in words if w not in stop_words]
        
        # Common topics mapping
        topic_map = {
            "anxious": "anxiety",
            "worried": "anxiety",
            "fear": "fear",
            "scared": "fear",
            "sad": "sadness",
            "depressed": "depression",
            "happy": "joy",
            "joyful": "joy",
            "angry": "anger",
            "mad": "anger",
            "tired": "weariness",
            "stressed": "stress",
            "peace": "peace",
            "love": "love",
            "hope": "hope",
            "faith": "faith"
        }
        
        for word in filtered:
            if word in topic_map:
                return topic_map[word]
        
        return " ".join(filtered[:3]) if filtered else "encouragement"
    
    def _detect_mood(self, message: str) -> str:
        """Detect user mood from message"""
        positive_words = ["happy", "joy", "blessed", "thankful", "grateful", "excited"]
        negative_words = ["sad", "anxious", "worried", "afraid", "angry", "tired", "stressed"]
        
        if any(word in message for word in positive_words):
            return "positive"
        elif any(word in message for word in negative_words):
            return "negative"
        return "neutral"
    
    def decide_action(self, intent_data: Dict[str, Any], user_data: Dict[str, Any]) -> str:
        """Decide which agent to call based on intent"""
        intent = intent_data.get("intent")
        
        action_map = {
            "daily_study": "bible_matcher",
            "daily_checkin": "memory",
            "verse_request": "bible_matcher",
            "bookmark": "memory",
            "progress": "memory",
            "greeting": "response_composer",
            "help": "response_composer",
            "conversation": "response_composer",
            "prayer": "response_composer"
        }
        
        return action_map.get(intent, "response_composer")

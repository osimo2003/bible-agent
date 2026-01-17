from fastapi import APIRouter, Request, Depends, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
from sqlalchemy.orm import Session
import logging
from app.database import get_db
from app.agents.planner import PlannerAgent
from app.agents.bible_matcher import BibleMatchingAgent
from app.agents.memory import MemoryAgent
from app.agents.response_composer import ResponseComposerAgent
from app.agents.scheduler import SchedulerAgent

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def whatsapp_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle incoming WhatsApp messages"""
    
    # Parse form data
    form_data = await request.form()
    from_number = form_data.get("From", "")
    message_body = form_data.get("Body", "").strip()
    
    logger.info(f"Message from {from_number}: {message_body}")
    
    # Initialize agents
    planner = PlannerAgent()
    bible_matcher = BibleMatchingAgent()
    memory = MemoryAgent(db)
    composer = ResponseComposerAgent()
    
    # Get or create user
    user = memory.get_or_create_user(from_number)
    
    # Save user message
    memory.save_conversation(
        user.id, 
        "user_message", 
        message_body,
        metadata={"phone_number": from_number}
    )
    
    # Analyze intent
    intent_data = planner.analyze_intent(message_body)
    action = planner.decide_action(intent_data, {"user_id": user.id})
    
    # Process based on action
    response_text = ""
    
    if action == "bible_matcher":
        if intent_data.get("intent") == "daily_study":
            # Get daily reading
            reading_data = bible_matcher.get_daily_reading(
                user.current_book, 
                user.last_chapter
            )
            reading_data['reflection_question'] = bible_matcher.generate_reflection_question(
                reading_data['book'], 
                reading_data['chapter_start']
            )
            
            # Get user stats
            stats = memory.get_user_stats(user.id)
            response_text = composer.compose_daily_reading_response(reading_data, stats)
            
        elif intent_data.get("intent") == "verse_request":
            # Find verses by topic
            topic = intent_data.get("topic", "encouragement")
            verses = bible_matcher.find_verses_by_topic(topic)
            response_text = composer.compose_verse_response(verses, topic)
    
    elif action == "memory":
        if intent_data.get("intent") == "daily_checkin":
            # User completed reading
            memory.update_user_progress(
                user.id,
                user.current_book,
                user.last_chapter,
                user.last_chapter + 2  # Assuming they read 2 chapters
            )
            response_text = "✅ Great job completing today's reading!\n\nGod's word is a lamp to your feet. See you tomorrow! 🙏"
        
        elif intent_data.get("intent") == "bookmark":
            verse_ref = intent_data.get("verse")
            if verse_ref:
                memory.add_bookmark(user.id, verse_ref)
                response_text = composer.compose_bookmark_saved(verse_ref)
            else:
                response_text = "Please specify a verse to bookmark. Example: SAVE John 3:16"
        
        elif intent_data.get("intent") == "progress":
            stats = memory.get_user_stats(user.id)
            response_text = composer.compose_progress_response(stats)
    
    elif action == "response_composer":
        if intent_data.get("intent") == "greeting":
            response_text = composer.compose_greeting()
        elif intent_data.get("intent") == "help":
            response_text = composer.compose_greeting()  # Same as greeting for now
        else:
            response_text = composer.compose_verse_response(
                bible_matcher.find_verses_by_topic("encouragement"), 
                "encouragement"
            )
    
    # Save agent response
    memory.save_conversation(
        user.id,
        "agent_response",
        response_text,
        intent=intent_data.get("intent")
    )
    
    # Create Twilio response
    twilio_response = MessagingResponse()
    twilio_response.message(response_text)
    
    return str(twilio_response)

@router.get("/webhook")
async def verify_webhook(request: Request):
    """Verify webhook for Twilio"""
    # Twilio requires GET endpoint for webhook verification
    return {"status": "Webhook is active"}

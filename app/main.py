# app/main.py - ENHANCED DEBUG VERSION
from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bible Agent Running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """Enhanced debug version"""
    try:
        logger.info("=" * 50)
        logger.info("📱 WEBHOOK CALLED - Processing WhatsApp message")
        
        # Get form data
        form_data = await request.form()
        
        # Log everything we receive
        logger.info(f"📦 Form data received: {dict(form_data)}")
        
        message = form_data.get("Body", "").strip()
        from_number = form_data.get("From", "")
        
        logger.info(f"💬 Message: '{message}'")
        logger.info(f"📞 From: {from_number}")
        
        # Create response
        response = MessagingResponse()
        
        if not message:
            response.message("Welcome! Please send a message like HELLO to start.")
        elif message.lower() in ["hello", "hi", "hey"]:
            response.message("""🙏 Hello! Welcome to Bible Agent!

📖 I'm here to help you study the Bible daily.

Try these commands:
• DAILY - Get today's reading
• VERSE - Find Bible verses
• HELP - See all commands

What would you like to do?""")
        elif "daily" in message.lower():
            response.message("""📖 *DAILY BIBLE STUDY*

Today's Reading: Matthew 1-2

💭 Reflection Question:
What does Jesus' genealogy teach us about God's faithfulness?

⏰ Take 10 minutes to read and reflect.

Reply READ when finished.""")
        elif "help" in message.lower():
            response.message("""📚 *BIBLE AGENT HELP*

Available Commands:
• HELLO - Start conversation
• DAILY - Today's Bible reading
• VERSE - Find verses by topic
• PROGRESS - Check your stats
• PRAYER - Share prayer request

Start with DAILY for today's reading!""")
        else:
            response.message(f"""I received: "{message}"

Type HELP to see all available commands, or try:
• HELLO - To start
• DAILY - For today's reading""")
        
        logger.info(f"📤 Sending response: {response}")
        logger.info("=" * 50)
        
        return str(response)
        
    except Exception as e:
        logger.error(f"❌ ERROR: {str(e)}", exc_info=True)
        response = MessagingResponse()
        response.message("Sorry, I encountered an error. Please try again in a moment.")
        return str(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

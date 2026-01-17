# app/main.py - SIMPLE WORKING VERSION
from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bible Agent Running", "status": "ok"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/webhook")
async def whatsapp_webhook(request: Request):
    """Handle WhatsApp messages"""
    try:
        form_data = await request.form()
        message = form_data.get("Body", "").strip()
        
        response = MessagingResponse()
        
        if message.lower() == "hello":
            response.message("🙏 Hello! Welcome to Bible Agent! Type DAILY for today's reading.")
        elif "daily" in message.lower():
            response.message("📖 *DAILY READING*\n\nMatthew 1-2\n\nReflection: What stands out to you?\n\nReply READ when done.")
        elif "verse" in message.lower():
            response.message("📖 *ENCOURAGING VERSES*\n\n1. John 3:16\n2. Philippians 4:6-7\n3. Isaiah 41:10\n\nWhich one speaks to you today?")
        elif "help" in message.lower():
            response.message("📚 *COMMANDS*\n\nHELLO - Greeting\nDAILY - Today's reading\nVERSE - Bible verses\nHELP - This message")
        else:
            response.message("Type HELP to see all commands. God bless! 🙏")
        
        return str(response)
    except Exception as e:
        response = MessagingResponse()
        response.message("Sorry, I encountered an error. Please try again.")
        return str(response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

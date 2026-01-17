from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv


load_dotenv()


from app.routes import whatsapp, users, bible
from app.database import engine, Base
from app.agents.scheduler import SchedulerAgent
from app.database import SessionLocal


Base.metadata.create_all(bind=engine)

scheduler = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    global scheduler
    db = SessionLocal()
    scheduler = SchedulerAgent(db)
    scheduler.start()
    print("🚀 Bible Agent started with scheduler")
    
    yield
    
   
    if scheduler:
        scheduler.shutdown()
    db.close()
    print("👋 Bible Agent stopped")


app = FastAPI(
    title="Bible Study WhatsApp Agent",
    description="AI-powered Bible study companion on WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(whatsapp.router, prefix="/api/whatsapp", tags=["WhatsApp"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(bible.router, prefix="/api/bible", tags=["Bible"])

@app.get("/")
async def root():
    return {
        "message": "Bible Study WhatsApp Agent API",
        "status": "running",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "bible-agent"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

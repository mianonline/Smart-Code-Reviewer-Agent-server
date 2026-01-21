from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from database import connect_to_mongo, close_mongo_connection
from routes import auth, users, review, chat, sessions
from models.schemas import HealthResponse
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Allowed Origins: {settings.ALLOWED_ORIGINS}")
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Smart Code Reviewer API",
    description="API for AI-powered code review (Refactored)",
    version="1.1.0",
    lifespan=lifespan
)

from fastapi import Request
import time

# Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    print(f"DEBUG: {request.method} {request.url.path} - Status: {response.status_code} - Origin: {request.headers.get('origin')} - Time: {formatted_process_time}ms")
    return response

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|\[::1\]|.*\.vercel\.app)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(review.router)
app.include_router(chat.router)
app.include_router(sessions.router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Smart Code Reviewer API is running. Visit /docs for documentation."}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "Service is running"
    }

if __name__ == "__main__":
    import os
    reload = os.getenv("DEBUG", "True").lower() == "true"
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=reload)

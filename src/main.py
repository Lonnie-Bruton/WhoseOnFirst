"""
WhoseOnFirst API - Main FastAPI Application

This module defines the main FastAPI application for the WhoseOnFirst
on-call rotation and SMS notification system.
"""

from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from src.api.routes import team_members, shifts, schedules
from src.scheduler import get_schedule_manager


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan context manager.

    Handles application startup and shutdown events:
    - Startup: Initialize and start the APScheduler
    - Shutdown: Stop the scheduler gracefully
    """
    # Startup
    logger.info("Starting WhoseOnFirst API...")

    # Initialize and start the scheduler
    try:
        scheduler = get_schedule_manager()
        scheduler.start()
        logger.info("Scheduler started successfully")

        # Log the next run time
        job_status = scheduler.get_job_status()
        if job_status:
            logger.info("Next notification job run: %s", job_status['next_run_time'])
    except Exception as e:
        logger.error("Failed to start scheduler: %s", str(e))
        raise

    yield

    # Shutdown
    logger.info("Shutting down WhoseOnFirst API...")

    # Stop the scheduler
    try:
        scheduler = get_schedule_manager()
        scheduler.stop(wait=True)
        logger.info("Scheduler stopped successfully")
    except Exception as e:
        logger.error("Error stopping scheduler: %s", str(e))


app = FastAPI(
    title="WhoseOnFirst API",
    description="Automated on-call rotation and SMS notification system for technical teams",
    version="0.2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware configuration
# Allow frontend to communicate with API during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Alternative frontend port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint returning API information.

    Returns:
        dict: API name and version
    """
    return {
        "name": "WhoseOnFirst API",
        "version": "0.2.0",
        "description": "On-call rotation and SMS notification system",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns:
        dict: Health status
    """
    return {
        "status": "healthy",
        "service": "whoseonfirst-api",
        "version": "0.2.0"
    }


# Include API routers
app.include_router(
    team_members.router,
    prefix="/api/v1/team-members",
    tags=["team-members"]
)
app.include_router(
    shifts.router,
    prefix="/api/v1/shifts",
    tags=["shifts"]
)
app.include_router(
    schedules.router,
    prefix="/api/v1/schedules",
    tags=["schedules"]
)

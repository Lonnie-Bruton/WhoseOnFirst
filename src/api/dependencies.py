"""
FastAPI Dependencies

This module provides dependency injection functions for FastAPI routes,
primarily for database session management.
"""

from typing import Generator
from sqlalchemy.orm import Session
from src.models.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.

    This dependency creates a new SQLAlchemy session for each request
    and ensures it is properly closed after the request is complete,
    even if an exception occurs.

    Yields:
        Session: SQLAlchemy database session

    Example:
        ```python
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

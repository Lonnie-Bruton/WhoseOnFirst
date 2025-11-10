#!/usr/bin/env python3
"""
Seed initial users for authentication.

Creates default admin and viewer accounts:
- admin / Admin123!
- viewer / Viewer123!
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy.orm import Session

from src.models.database import SessionLocal
from src.models.user import User, UserRole
from src.auth.utils import hash_password


def seed_users(db: Session):
    """
    Seed default admin and viewer users.

    Args:
        db: Database session
    """
    # Check if users already exist
    existing_admin = db.query(User).filter(User.username == "admin").first()
    existing_viewer = db.query(User).filter(User.username == "viewer").first()

    if existing_admin and existing_viewer:
        print("✅ Default users already exist. Skipping seed.")
        return

    # Create admin user
    if not existing_admin:
        admin = User(
            username="admin",
            password_hash=hash_password("Admin123!"),
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(admin)
        print("✅ Created admin user (username: admin, password: Admin123!)")
    else:
        print("ℹ️  Admin user already exists")

    # Create viewer user
    if not existing_viewer:
        viewer = User(
            username="viewer",
            password_hash=hash_password("Viewer123!"),
            role=UserRole.VIEWER,
            is_active=True
        )
        db.add(viewer)
        print("✅ Created viewer user (username: viewer, password: Viewer123!)")
    else:
        print("ℹ️  Viewer user already exists")

    # Commit changes
    db.commit()
    print("\n🎉 User seeding completed successfully!")


def main():
    """Main entry point."""
    print("🌱 Seeding default users...")

    # Create database session
    db = SessionLocal()

    try:
        seed_users(db)
    except Exception as e:
        print(f"❌ Error seeding users: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

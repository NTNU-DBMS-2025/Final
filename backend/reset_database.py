#!/usr/bin/env python3
"""
Reset the database with new schema and data
"""

from app import create_app
from models import db
import subprocess
import os


def reset_database():
    """Drop all tables and recreate with new schema"""
    app = create_app()

    with app.app_context():
        print("🗑️  Dropping all existing tables...")
        db.drop_all()

        print("📋 Creating tables from new schema...")
        db.create_all()

        print("✅ Database reset complete!")
        print("Now run 'python init_data.py' to populate with sample data")


if __name__ == "__main__":
    reset_database()

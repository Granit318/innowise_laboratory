"""
Database Configuration Module

This module handles database connection setup and session management.
It provides SQLAlchemy engine and session factory for database operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine for SQLite database
# The engine is the starting point for any SQLAlchemy application
engine = create_engine(
    "sqlite:///books.db",  # Database URL - SQLite file named 'books.db' in current directory
    echo=True,  # Enable SQL query logging to console (useful for debugging)
)

# Create session factory (SessionLocal) bound to the engine
# This factory will produce individual database sessions
SessionLocal = sessionmaker(
    bind=engine,  # Bind sessions to the created engine
    autoflush=False,  # Disable autoflush - changes won't be automatically flushed to database
    autocommit=False,  # Disable autocommit - transactions must be explicitly committed
)

# Usage Example:
# from this_module import SessionLocal
# db = SessionLocal()
# try:
#     # Perform database operations
#     books = db.query(Book).all()
#     db.commit()
# finally:
#     db.close()

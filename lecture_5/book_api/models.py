"""
SQLAlchemy ORM Models for Books Management System

This module defines the database models using SQLAlchemy 2.0 declarative base.
It provides the Book model for storing book information in the database.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy ORM models.

    This class serves as the foundation for declarative class definitions.
    All models should inherit from this class to ensure proper integration
    with SQLAlchemy's metadata and configuration systems.

    Attributes:
        None (acts as a marker class for SQLAlchemy)

    Example:
        >>> class User(Base):
        ...     __tablename__ = 'users'
        ...     id = mapped_column(Integer, primary_key=True)
    """

    ...


class Book(Base):
    """
    ORM Model representing a book in the database.

    This class maps to the 'book' table in the database and defines
    the structure for storing book information including title,
    author, and publication year.

    Attributes:
        id (Mapped[int]): Primary key identifier for the book
        title (Mapped[str]): Title of the book (max 50 characters)
        author (Mapped[str]): Author of the book (max 50 characters)
        year (Mapped[Optional[int]]): Publication year (nullable)

    Table Schema:
        CREATE TABLE book (
            id INTEGER PRIMARY KEY,
            title VARCHAR(50) NOT NULL,
            author VARCHAR(50) NOT NULL,
            year INTEGER
        );

    Example:
        >>> book = Book(
        ...     title="The Great Gatsby",
        ...     author="F. Scott Fitzgerald",
        ...     year=1925
        ... )
        >>> print(book.title)
        'The Great Gatsby'
    """

    __tablename__ = "book"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)
    author: Mapped[str] = mapped_column(String(50), nullable=False)
    year: Mapped[str | None] = mapped_column(Integer, nullable=True)

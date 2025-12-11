"""
FastAPI Application for Books Management API

This module provides REST API endpoints for managing books in a database.
It includes CRUD operations and search functionality.
"""

import base
import models
import schemas
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

# Create database tables
models.Base.metadata.create_all(bind=base.engine)

# Initialize FastAPI application
app = FastAPI(
    title="Books Management API",
    description="A REST API for managing books with CRUD operations and search functionality",
    version="1.0.0",
)


def get_db():
    """
    Database dependency generator for FastAPI.

    Yields:
        Session: SQLAlchemy database session

    Example:
        >>> db = next(get_db())
        >>> books = db.query(models.Book).all()
    """
    db = base.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/books",
    response_model=schemas.BookDBSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new book",
    description="Creates a new book record in the database with the provided details",
)
def create_book(book: schemas.BookCreateSchema, db: Session = Depends(get_db)):
    """
    Create a new book in the database.

    Args:
        book (BookCreateSchema): Book data including title, author, and optional year
        db (Session): Database session dependency

    Returns:
        BookDBSchema: Created book record with assigned ID

    Raises:
        HTTPException: If database constraints are violated

    Example:
        POST /books
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "year": 1925
        }
    """
    # Create new book instance from request data
    db_book = models.Book(title=book.title, author=book.author, year=book.year)

    # Save to database
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    return db_book


@app.get(
    "/books",
    response_model=list[schemas.BookDBSchema],
    status_code=status.HTTP_200_OK,
    summary="Get all books",
    description="Retrieves a list of all books in the database",
)
def get_books(db: Session = Depends(get_db)):
    """
    Retrieve all books from the database.

    Args:
        db (Session): Database session dependency

    Returns:
        list[BookDBSchema]: List of all book records

    Example:
        GET /books
    """
    return db.query(models.Book).all()


@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a book",
    description="Deletes a specific book by its ID",
)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by its ID.

    Args:
        book_id (int): ID of the book to delete
        db (Session): Database session dependency

    Raises:
        HTTPException: 404 if book with specified ID is not found

    Example:
        DELETE /books/1
    """
    # Find the book by ID
    book = db.get(models.Book, book_id)

    # Check if book exists
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # Delete the book
    db.delete(book)
    db.commit()

    # Return 204 No Content on successful deletion


@app.put(
    "/books/{book_id}",
    response_model=schemas.BookDBSchema,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Update a book",
    description="Updates all fields of a specific book by its ID",
)
def update_book(
    book_id: int, update_data: schemas.BookUpdateSchema, db: Session = Depends(get_db)
):
    """
    Update a book's information by its ID.

    Note: This is a PUT endpoint that updates all fields.
    Use PATCH for partial updates.

    Args:
        book_id (int): ID of the book to update
        update_data (BookUpdateSchema): New data for the book
        db (Session): Database session dependency

    Returns:
        BookDBSchema: Updated book record

    Raises:
        HTTPException: 404 if book with specified ID is not found
        HTTPException: 400 if no update data is provided

    Example:
        PUT /books/1
        {
            "title": "Updated Title",
            "author": "Updated Author",
            "year": 2023
        }
    """
    # Find the book by ID
    db_book = db.get(models.Book, book_id)

    # Check if book exists
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )

    # Check if update data is provided
    # Note: In a PUT request, we typically require all fields
    # For partial updates, consider using PATCH method
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No update data provided"
        )

    # Update book fields
    db_book.title = update_data.title
    db_book.author = update_data.author
    db_book.year = update_data.year

    # Save changes to database
    db.commit()

    return db_book


@app.get(
    "/books/search",
    response_model=list[schemas.BookDBSchema],
    summary="Search books",
    description="Search books by title, author, or filter by publication year",
)
def search_books(
    query: str | None = Query(
        None,
        description="Search term to match in book title or author (case-insensitive partial match)",
    ),
    year: int | None = Query(
        None, description="Exact publication year to filter books"
    ),
    db: Session = Depends(get_db),
) -> list[schemas.BookDBSchema]:
    """
    Search for books by title, author, or publication year.

    Args:
        query (str | None): Search term to match in title or author fields.
                           Performs case-insensitive partial matching.
        year (int | None): Exact publication year to filter results.
        db (Session): Database session dependency.

    Returns:
        list[BookDBSchema]: List of books matching the search criteria,
                           sorted by title in ascending order.

    Example:
        GET /books/search?query=gatsby&year=1925
        GET /books/search?query=love
        GET /books/search?year=2020

    Notes:
        - If both query and year are provided, results must satisfy both conditions
        - Query searches in both title and author fields using OR logic
        - Search is case-insensitive (ilike)
        - Results are ordered by title
    """
    # Start with base query
    db_query = db.query(models.Book)

    # Apply search term filter if provided
    if query:
        search_term = f"%{query}%"
        db_query = db_query.filter(
            or_(
                models.Book.title.ilike(search_term),
                models.Book.author.ilike(search_term),
            )
        )

    # Apply year filter if provided
    if year is not None:
        db_query = db_query.filter(models.Book.year == year)

    # Execute query and order results by title
    books = db_query.order_by(models.Book.title).all()

    # Convert SQLAlchemy objects to Pydantic models
    # Note: This explicit conversion ensures proper serialization
    result_books = []
    for book in books:
        # Create dictionary from book object, excluding SQLAlchemy internal attributes
        book_dict = {k: v for k, v in book.__dict__.items() if not k.startswith("_")}
        result_books.append(schemas.BookDBSchema(**book_dict))

    return result_books


# Optional: Add health check endpoint
@app.get(
    "/health",
    summary="Health check",
    description="Check if the API is running properly",
)
def health_check():
    """
    Health check endpoint to verify API is operational.

    Returns:
        dict: Status information

    Example:
        GET /health
    """
    return {"status": "healthy", "service": "books-management-api", "version": "1.0.0"}

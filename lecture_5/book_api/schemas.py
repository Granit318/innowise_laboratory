from pydantic import BaseModel, Field, field_validator


class BookUpdateSchema(BaseModel):
    """
    Pydantic schema for updating book information.

    This schema is used for PUT/PATCH requests to update existing books.
    All fields are required for complete updates, but can be used with
    partial=True for partial updates.
    """

    title: str = Field(
        max_length=50, min_length=1, description="Title of the book (1-50 characters)"
    )
    author: str = Field(
        max_length=50, min_length=1, description="Author of the book (1-50 characters)"
    )
    year: int | None = Field(
        None, description="Publication year of the book. Can be None/null."
    )

    @classmethod
    @field_validator("year", mode="before")
    def validate_year_string(cls, value):
        """
        Validator for the 'year' field that handles string inputs.

        This validator runs BEFORE type conversion (mode="before") and
        validates/transforms the year value.

        Args:
            value: The input value for the year field

        Returns:
            int | None: Validated year as integer or None

        Raises:
            ValueError: If the value is a non-empty string (strings are not accepted)

        Note:
            - None values are passed through as None
            - Empty strings are converted to None
            - Non-empty strings raise ValueError (only integers are accepted)
            - Integer values are passed through unchanged
        """
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
            else:
                raise ValueError("Year must be a valid integer, not a string")
        # If value is already an integer, it passes through unchanged
        return value


class BookCreateSchema(BookUpdateSchema):
    """
    Pydantic schema for creating new books.

    Inherits all fields and validators from BookUpdateSchema.
    Used for POST requests when creating new book records.

    Note:
        This class currently has the same fields as BookUpdateSchema,
        but can be extended with additional validation or fields
        specific to book creation if needed in the future.
    """

    ...


class BookDBSchema(BookCreateSchema):
    """
    Pydantic schema for book data retrieved from the database.

    Inherits all fields from BookCreateSchema and adds an 'id' field.
    This schema represents the complete book record as stored in the database.

    Used for response models in API endpoints to ensure consistent
    data structure in responses.
    """

    id: int = Field(
        ...,  # Ellipsis indicates this field is required
        description="Unique identifier (primary key) of the book in the database",
    )

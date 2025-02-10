from typing import OrderedDict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )


@router.get(
    "/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK
)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()


@router.get("/{book_id}",
    response_model=Book,
    responses={
        404: {
            "description": "Not Found Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Book not found"
                    }
                }
            }
        }
    },
    status_code=status.HTTP_200_OK
)
async def get_book(book_id: int) -> Book:
    """
    Return a book with all the information:
    
    - **id**: Unique identifier for the book.
    - **title**: Title of the book.
    - **author**: Author of the book.
    - **publication_year**: Year the book was published.
    - **genre**: Genre of the book.
    \f
    :param book_id: Book ID.
    """
    book_data = db.get_book(book_id)
    if book_data:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=book_data.model_dump()
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Book not found"},
        )


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=db.update_book(book_id, book).model_dump(),
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int) -> None:
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)

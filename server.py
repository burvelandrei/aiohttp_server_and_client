from aiohttp import web
import json
from pydantic import BaseModel, ValidationError


class BookModel(BaseModel):
    id: int
    name: str


books = {
    1: "Мастер и Маргарита",
    2: "Собачье сердце",
}


async def get_books(request):
    return web.json_response(books)


async def get_book(request):
    book_id = int(request.match_info["id"])
    book = books.get(book_id)
    if book:
        return web.json_response({book_id: book})
    return web.json_response({"error": "Book not found"}, status=404)


async def add_book(request):
    try:
        body = await request.json()
        book = BookModel(**body)
        if book.id not in books:
            books[book.id] = book.name
            print(f"Book added: {book.name}")
            return web.json_response({"message": "Book added"}, status=201)
        else:
            print(f"Attempt to add existing book: {book.name}")
            return web.json_response({"error": "The book already exists"}, status=400)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return web.json_response(
            {"error": "JSON is incorrect, id, name are missing"}, status=400
        )
    except json.decoder.JSONDecodeError:
        print("Invalid JSON received")
        return web.json_response({"error": "JSON invalid"}, status=400)


async def update_book(request):
    try:
        body = await request.json()
        book = BookModel(**body)
        if book.id in books:
            books[book.id] = book.name
            print(f"Book updated: {book.name}")
            return web.json_response({"message": "Book updated"}, status=200)
        else:
            print(f"Attempt to update non-existing book: {book.name}")
            return web.json_response({"error": "Book not found"}, status=404)
    except ValidationError as e:
        print(f"Validation error: {e}")
        return web.json_response(
            {"error": "JSON is incorrect, id, name are missing"}, status=400
        )
    except json.decoder.JSONDecodeError:
        print("Invalid JSON received")
        return web.json_response({"error": "JSON invalid"}, status=400)


async def delete_book(request):
    book_id = int(request.match_info["id"])
    if book_id in books:
        del books[book_id]
        print(f"Book deleted: {book_id}")
        return web.json_response(status=204)
    print(f"Attempt to delete non-existing book: {book_id}")
    return web.json_response({"error": "Book not found"}, status=404)


async def create_app():
    app = web.Application()
    app.add_routes(
        [
            web.get("/books/", get_books),
            web.get("/books/{id}/", get_book),
            web.post("/add_book/", add_book),
            web.post("/update_book/", update_book),
            web.delete("/delete_book/{id}/", delete_book),
        ]
    )
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="127.0.0.1", port=8080)

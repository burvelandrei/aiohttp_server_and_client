from aiohttp import web, request
import json


books = {
    "1": "b",
    "2": "c"
}

app = web.Application()

async def get_books(request):
    return web.json_response(books)


app.router.add_get("/", get_books)

if __name__ == "__main__":
    web.run_app(app)
import asyncio
from environs import Env
from aiohttp import client


env = Env()
env.read_env()


class APIClient:
    def __init__(self):
        self.domain = f"http://{env('HOST')}:{env('PORT')}"

    async def __aenter__(self):
        self.session = client.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get_books(self):
        url = f"{self.domain}/books/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    print(response.status)
                    print(await response.json())
                else:
                    print(f"Ошибка GET запроса - {response.status}")
        except client.ClientError as e:
            print(f"Ошибка сети - {e}")

    async def get_book(self, id):
        url = f"{self.domain}/books/{id}/"
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    print(response.status)
                    print(await response.json())
                else:
                    print(f"Ошибка GET запроса - {response.status}")
        except client.ClientError as e:
            print(f"Ошибка сети - {e}")

    async def add_book(self, data):
        url = f"{self.domain}/add_book/"
        try:
            async with self.session.post(url, json=data) as response:
                if response.status == 201:
                    print(response.status)
                    print(await response.json())
                else:
                    print(
                        f"Ошибка POST запроса - {response.status}, {await response.json()}"
                    )
        except client.ClientError as e:
            print(f"Ошибка сети - {e}")

    async def update_book(self, data):
        url = f"{self.domain}/update_book/"
        try:
            async with self.session.patch(url, json=data) as response:
                if response.status == 200:
                    print(response.status)
                    print(await response.json())
                else:
                    print(
                        f"Ошибка PATCH запроса - {response.status}, {await response.json()}"
                    )
        except client.ClientError as e:
            print(f"Ошибка сети - {e}")

    async def delete_book(self, id):
        url = f"{self.domain}/delete_book/{id}/"
        try:
            async with self.session.delete(url) as response:
                if response.status == 204:
                    print(response.status)
                    print(await response.json())
                else:
                    print(f"Ошибка DELETE запроса - {response.status}")
        except client.ClientError as e:
            print(f"Ошибка сети - {e}")


# Создаём таски для проверки
async def main():
    async with APIClient() as api:
        await asyncio.create_task(api.get_books())
        await asyncio.create_task(api.get_book(1))
        await asyncio.create_task(api.add_book({"id": 3, "name": "Война и мир"}))
        await asyncio.create_task(api.update_book({"id": 2, "name": "Собачье"}))
        await asyncio.create_task(api.delete_book(2))


if __name__ == "__main__":
    asyncio.run(main())

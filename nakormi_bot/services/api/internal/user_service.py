from entities.user import User
from entities.inventory import InventoryLine
from services.common import BaseService
import httpx


class UserService(BaseService):
    def __init__(self, address: str, api_key: str, site_address: str):
        super().__init__(address, api_key, site_address)

    async def exists(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/edit/{user_id}',
                                        headers=headers)
            print(response.text)
            return response.status_code == 200

    async def register(self, user: User):
        headers = self.headers
        headers['Tg-Id'] = str(user.tg_id)

        # TODO: Add support for file upload
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{self.address}/edit/{user.tg_id}',
                                          headers=headers,
                                          data=user.__dict__)

            return response.status_code == 200

    async def update(self, user: User):
        headers = self.headers
        headers['Tg-Id'] = str(user.tg_id)

        # TODO: Add support for file upload
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{self.address}/edit/{user.tg_id}',
                                          headers=headers,
                                          data=user.__dict__)

            return response.status_code == 200

    async def get(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/edit/{user_id}',
                                        headers=headers)
            data = response.json()
            data['tg_id'] = user_id
            return User(**data)

    async def inventory(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/inventory/',
                                        headers=headers)
            data = response.json()
            return [InventoryLine(**item) for item in data]

    async def check(self, user_id: int, searched_user: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/check/{searched_user}',
                                        headers=headers)
            return response.status_code == 200

    async def share_feed(self, from_user: int, to_user: int, content: dict):
        headers = self.headers
        headers['Tg-Id'] = str(from_user)

        async with httpx.AsyncClient() as client:
            body = {"content": content, "action": 2, "from_user": from_user, "to_user": to_user}
            response = await client.post(f'{self.address}/share_feed/',
                                         headers=headers, json=body)
            return response.status_code == 200, response.json()

    async def usage_feed(self, from_user: int, content: dict, district: int):
        headers = self.headers
        headers['Tg-Id'] = str(from_user)

        async with httpx.AsyncClient() as client:
            body = {"content": content, "action": 3, "from_user": from_user, "district": district}
            response = await client.post(f'{self.address}/usage_feed/',
                                         headers=headers, json=body)
            return response.status_code == 200, response.json()
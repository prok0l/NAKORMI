from entities.user import User
from entities.inventory import InventoryLine
from services.common import BaseService
import httpx


class MainService(BaseService):
    def __init__(self, address: str, api_key: str, site_address: str):
        super().__init__(address, api_key, site_address)

    async def get_districts(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/districts/',
                                        headers=headers)
            return response.json()

    async def upload(self, file, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.address}/photo/upload/', files={'photo': file},
                                         headers=headers)
            print(response)
            return response.json()
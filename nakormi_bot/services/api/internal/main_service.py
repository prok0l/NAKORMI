from nakormi_bot.entities.user import User
from nakormi_bot.entities.inventory import InventoryLine
from nakormi_bot.services.common import BaseService
import httpx


class MainService(BaseService):
    def __init__(self, address: str, api_key: str):
        super().__init__(address, api_key)

    async def get_districts(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/districts/',
                                        headers=headers)
            return response.json()
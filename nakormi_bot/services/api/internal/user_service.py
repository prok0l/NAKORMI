from nakormi_bot.entities.user import User
from nakormi_bot.services.common import BaseService
import httpx


class UserService(BaseService):
    def __init__(self, address: str, api_key: str):
        super().__init__(address, api_key)

    async def exists(self, user_id: int):
        headers = super().headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/edit',
                                        headers=headers)

            return response.status_code == 200

    async def register(self, user: User):
        headers = super().headers
        headers['Tg-Id'] = str(user.telegram_id)

        # TODO: Add support for file upload
        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{self.address}/edit',
                                          headers=headers,
                                          data=user.__dict__)

            return response.status_code == 200

    async def get(self, user_id: int):
        headers = super().headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/edit',
                                        headers=headers)

            return User(**response.json())

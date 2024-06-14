from entities.tag import Tag
from nakormi_bot.entities.user import User
from nakormi_bot.services.common import BaseService
import httpx


class FeedService(BaseService):
    def __init__(self, address: str, api_key: str, site_address):
        super().__init__(address, api_key, site_address)

    async def tags(self, user_id: int, level: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/tags/{level}',
                                        headers=headers)
            data = response.json()
            return [Tag(**item) for item in data.get('tags')]
from entities.tag import Tag
from entities.user import User
from services.common import BaseService
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

    async def report_photo(self, user_id: int, report_id: int, file):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.post(f'{self.address}/reports/photo/',
                                        headers=headers,
                                        files={'photo': file},
                                         data={'report': report_id,
                                               'tg_id': user_id})
            return response.json()

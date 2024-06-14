from entities.user import User
from services.common import BaseService
import httpx


class PointService(BaseService):
    def __init__(self, address: str, api_key: str, site_address: str):
        super().__init__(address, api_key, site_address)

    async def get_points(self, user_id: int):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            response = await client.get(f'{self.address}/points/',
                                        headers=headers)
            return response.json()

    async def take(self, user_id: int, point_id: int, content: dict):
        headers = self.headers
        headers['Tg-Id'] = str(user_id)

        async with httpx.AsyncClient() as client:
            body = {"content": content, "action": 1, "to_user": user_id, "point": point_id}
            response = await client.post(f'{self.address}/take/{point_id}',
                                         headers=headers, json=body)
            return response.status_code == 200

    @property
    def map(self):
        return f'{self.site_address}/map/'

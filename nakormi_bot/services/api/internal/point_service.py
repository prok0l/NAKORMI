from entities.point import Point
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
            return response.json()

    @property
    def map(self):
        return f'{self.site_address}/map/'

    async def create_point(self, from_user: int, point_obj: Point, file):
        headers = self.headers
        headers['Tg-Id'] = str(from_user)

        async with httpx.AsyncClient() as client:
            data = {k: v for k, v in point_obj.__dict__.items() if v}
            response = await client.post(f'{self.address}/points/', headers=headers,
                                         data=data,
                                         files=file)

    async def update_point(self, from_user: int, data):
        headers = self.headers
        headers['Tg-Id'] = str(from_user)

        data.pop('photo')

        async with httpx.AsyncClient() as client:
            response = await client.patch(f'{self.address}/points/{data["id"]}', headers=headers,
                                         data=data)

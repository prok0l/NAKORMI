from nakormi_bot.entities.user import User
from nakormi_bot.services.common import BaseService
import httpx


class FeedService(BaseService):
    def __init__(self, address: str, api_key: str):
        super().__init__(address, api_key)
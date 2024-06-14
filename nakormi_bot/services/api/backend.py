from nakormi_bot.services.api.internal.user_service import UserService
from nakormi_bot.services.api.internal.feed_service import FeedService
from nakormi_bot.services.api.internal.main_service import MainService
from nakormi_bot.services.common import BaseService


class Backend(BaseService):
    """
    Бэкенд для работы с API "Накорми"
    """
    def __init__(self, address: str, api_key: str):
        super().__init__(address, api_key)

        self.users = UserService(f'{address}/user', api_key)
        # self.points = PointService(f'{address}/point', api_key)
        self.feed = FeedService(f'{address}/feed', api_key)
        self.main = MainService(f'{address}/main', api_key)
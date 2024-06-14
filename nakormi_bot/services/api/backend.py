from services.api.internal.user_service import UserService
from services.api.internal.feed_service import FeedService
from services.api.internal.main_service import MainService
from services.api.internal.point_service import PointService
from services.common import BaseService


class Backend(BaseService):
    """
    Бэкенд для работы с API "Накорми"
    """
    def __init__(self, address: str, api_key: str, site_address: str):
        super().__init__(address, api_key, site_address)

        self.users = UserService(f'{address}/user', api_key, site_address)
        self.points = PointService(f'{address}/point', api_key, site_address)
        self.feed = FeedService(f'{address}/feed', api_key, site_address)
        self.main = MainService(f'{address}/main', api_key, site_address)
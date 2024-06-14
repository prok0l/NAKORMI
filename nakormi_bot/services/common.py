class BaseService:
    def __init__(self, address: str, api_key: str, site_address: str):
        self.address = address
        self.api_key = api_key
        self.site_address = site_address

        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Api-Key {api_key}'
        }

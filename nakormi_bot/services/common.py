class BaseService:
    def __init__(self, address: str, api_key: str):
        self.address = address
        self.api_key = api_key

        self.headers = {
            'Accept': 'application/json',
            'Authorization': f'Api-Key {api_key}'
        }

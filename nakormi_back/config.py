from dotenv import load_dotenv
from dataclasses import dataclass
from os import getenv


@dataclass
class Config:
    username: str
    password: str
    host: str
    port: str
    db_name: str
    secret: str
    debug: bool = False


def load() -> Config:
    load_dotenv()
    conf = Config(
        username=getenv('DB_USER'),
        password=getenv('DB_PASSWORD'),
        host=getenv('DB_ADDRESS'),
        port=getenv('DB_PORT'),
        db_name=getenv('DB_NAME'),
        secret=getenv('RANDOM_SECRET'),
        debug=(getenv('DEBUG', 'False') == 'True'),
    )
    return conf

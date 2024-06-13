import json
from typing import Any


def __load_phrases__(phrases_path: str) -> Any:
    with open(phrases_path, 'r', encoding='utf-8') as path:
        return json.load(path)


class Phrases:
    def __init__(self, phrases_path: str = 'phrases_ru.json'):
        self.phrases = __load_phrases__(phrases_path)

    def __getitem__(self, item):
        return self.phrases[item]

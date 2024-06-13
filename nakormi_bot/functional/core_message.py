from datetime import datetime


class CoreMessage:
    """
    Главное сообщение в диалоге, которое редактируется при каждом ответе пользователя

    Используется принцип Single-Message-Dialog
    """
    def __init__(self, chat_id: int, message_id: int, telegram_id: int, date: datetime):
        self.chat_id = chat_id
        self.message_id = message_id
        self.telegram_id = telegram_id
        self.date = date

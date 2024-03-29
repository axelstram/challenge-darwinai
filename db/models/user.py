class User:
    def __init__(self, telegram_id):
        self.telegram_id = telegram_id

    def get_telegram_id(self):
        return self.telegram_id
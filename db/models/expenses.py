from datetime import datetime

class Expense:
    def __init__(self, user_telegram_id, description, amount, category, added_at=None):
        self.user_telegram_id = user_telegram_id
        self.description = description
        self.amount = amount
        self.category = category
        self.added_at = added_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
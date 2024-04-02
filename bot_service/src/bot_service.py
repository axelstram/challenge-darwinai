from bots.src.factory_registry import BotFactoryRegistry
from db.src.db_manager import DatabaseManager
from db.models.user import User
from db.models.expenses import Expense


class BotService:

    def __init__(self):
        self.db = DatabaseManager()
        self.bot_factory_registry = BotFactoryRegistry()
        self.bot = None

    def set_bot(self, bot_type):
        self.bot_factory = self.bot_factory_registry.get_factory(bot_type)
        self.bot = self.bot_factory.create_bot()

    def whitelist_user(self, user_id):
        user = User(user_id)

        if self.db.user_is_whitelisted(user):
            return f'response: user with id {user_id} has already been whitelisted'
        else:
            success = self.db.insert_user(user)

            if success:
                return f'response: user with id {user_id} has been whitelisted'
            else:
                return f'error: unexpected error while trying to whitelist user with id {user_id}'

    def is_whitelisted(self, user_id):
        user = User(user_id)

        return self.db.user_is_whitelisted(user)

    def has_bot(self):
        return self.bot

    def list_available_bots(self):
        return self.bot_factory_registry.list_factories()

    def process_message(self, message, user_id):
        response = self.bot.process_message(message)

        if response['Category'] == "None":
            return 'message did not contain information related to expenses'
        
        expense = Expense(user_telegram_id=user_id, description=response['Description'], amount=response['Amount'], category=response['Category'])
        
        success = self.db.insert_expense(expense)

        if success:
            return f'[{expense.category}] expense added ✓'
        else:
            return f'error: failed to add expense {expense}'

    def list_user_expenses(self, user_id):
        return self.db.get_expenses_from_user(User(user_id))



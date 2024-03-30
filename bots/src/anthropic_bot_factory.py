from bots.interfaces.bot_factory import BotFactory
from bots.src.anthropic_bot import AnthropicBot

class AnthropicBotFactory(BotFactory):

    def create_bot(self, api_key=None):
        return AnthropicBot(api_key)
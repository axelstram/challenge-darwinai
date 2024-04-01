from bots.src.anthropic_bot_factory import AnthropicBotFactory


class BotFactoryRegistry:
    def __init__(self):
        self.factories = {
            'anthropic': AnthropicBotFactory(),
            #If new bots are developed (e.g. bots using OpenAI or another llm), their factory would be registered here
            # ...
        }

    def get_factory(self, bot_type):
        factory = self.factories.get(bot_type)
        
        if factory is None:
            raise ValueError(f'Unsupported bot type: {bot_type}')
        return factory

    def list_factories(self):
        return list(self.factories.keys())
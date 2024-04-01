from bots.src.factory_registry import BotFactoryRegistry


def test_that_when_anthropic_bot_is_created_it_classifies_the_message_correctly():
    anthropic_factory = BotFactoryRegistry().get_factory('anthropic')
    bot = anthropic_factory.create_bot()
    message = "pizza 20 bucks"

    result = bot.process_message(message)

    assert result['Category'] == 'Food'
    assert result['Amount'] == '20'
    assert result['Description'] == 'Pizza'
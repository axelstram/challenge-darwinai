from fastapi.testclient import TestClient
from bot_service.src.request_handler import app
from bot_service.src.bot_service import BotService

bot_service = BotService()
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "App running"}


def test_that_whitelisted_user_is_added():
    response = client.post('/whitelist_user?user_id=666')
    assert response.status_code == 200
    response = client.get('/is_whitelisted?user_id=666')
    assert response.status_code == 200


def test_that_I_can_get_list_of_bots_and_set_one_appropiately():
    response = client.get('/list_available_bots')

    assert response.status_code == 200
    assert 'anthropic' in response.json()['bots']

def test_that_if_I_add_an_expense_it_is_added_correctly():
    user_id = '666'
    client.post('/whitelist_user?user_id=' + user_id)
    client.post('/set_bot?bot_type=anthropic')
    client.post('/process_message?user_id='+ user_id + '&message="netflix 1000 pesos"')
    response = client.get('/list_user_expenses?user_id='+ user_id)

    expense = response.json()['expenses'][0]

    assert expense['Description'] == 'Netflix'

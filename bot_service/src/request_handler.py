from bot_service.src.bot_service import BotService
from fastapi import FastAPI, HTTPException, status

app = FastAPI()
bot_service = BotService()


@app.get("/")
async def root():
    return {"message": "App running"}


@app.post('/set_bot')
async def set_bot(bot_type):
    try:
        bot_service.set_bot(bot_type)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {f'{bot_type} bot created successfully'}


@app.post('/whitelist_user')
async def whitelist_user(user_id):
    response = bot_service.whitelist_user(user_id)

    if 'error' in response:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)
    else:
        return {response}

@app.get('/is_whitelisted')
async def is_whitelisted(user_id):
    if bot_service.is_whitelisted(user_id):
        return {f' user_id {user_id} is whitelisted: True'}
    else:
        return {f' user_id {user_id} is whitelisted: False'}


@app.post('/process_message')
async def process_message(message, user_id):

    if not bot_service.is_whitelisted(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'error: user with id {user_id} is not whitelisted') 

    if bot_service.has_bot():
        response = bot_service.process_message(message, user_id)
        
        if 'error' in response:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=response)
        else:
            return {response}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'error: No bot instance available. Create a bot first. You can choose one from the following list: {bot_service.list_available_bots()}')


@app.get('/list_user_expenses')
async def list_user_expenses(user_id):
    if not bot_service.is_whitelisted(user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'error: user with id {user_id} is not whitelisted') 

    expenses = bot_service.list_user_expenses(user_id)

    return {'expenses': expenses}
    
@app.get('/list_available_bots')
async def list_available_bots():
    return {'bots': f'{bot_service.list_available_bots()}'}
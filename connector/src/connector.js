const axios = require("axios");
const TelegramBot = require('node-telegram-bot-api');

if (process.env.PRODUCTION != true) {
    require('dotenv').config();
}


const token = process.env.TELEGRAM_BOT_API_KEY;
const BOT_TYPE = process.env.BOT_TYPE;
const bot = new TelegramBot(token, {polling: true});
const URL = 'https://darwinai-n3s5o067.b4a.run';
const IS_WHITELISTED_ENDPOINT = '/is_whitelisted';
const LIST_USER_EXPENSES_ENDPOINT = '/list_user_expenses';
const WHITELIST_USER_ENDPOINT = '/whitelist_user';
const SET_BOT_ENDPOINT = '/set_bot';
const LIST_AVAILABLE_BOTS_ENDPOINT = '/list_available_bots';
const PROCESS_MESSAGE_ENDPOINT = '/process_message';


async function isWhitelisted(userId) {
    const response =  await axios.get(URL + IS_WHITELISTED_ENDPOINT + '?user_id=' + userId);

    if (response.data[0].includes('True')) {
        return true;
    } else {
        return false;
    }
}

function printExpenses(expenses) {
    let result = 'Expenses:\n';
  
    expenses.forEach((expense, index) => {
      result += `${index + 1}. Description: ${expense.Description}\n`;
      result += `   Amount: ${expense.Amount}\n`;
      result += `   Category: ${expense.Category}\n`;
      result += `   Date: ${expense.Date}\n`;
      result += '---\n';
    });
  
    return result;
  }


bot.on('message', async (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;
    let whitelisted;

    switch (msg.text) {

        //whitelist user
        case '/whitelist':
            axios.post(URL + WHITELIST_USER_ENDPOINT + '?user_id=' + userId).then(response => {
                bot.sendMessage(chatId, response.data[0]);
            })

            break;
        
        //List all of a user's expenses
        case '/expenses':
            whitelisted = await isWhitelisted(userId);

            if (whitelisted) {
                axios.get(URL + LIST_USER_EXPENSES_ENDPOINT + '?user_id=' + userId).then(response => {
                    bot.sendMessage(chatId, printExpenses(response.data['expenses']));
                })
            } else {
                bot.sendMessage(chatId, 'You are not whitelisted');
            }

            break;

        //List all commands
        case '/help':
            bot.sendMessage(chatId, 'help');
            break;
        
        //List all available bots
        case '/bots':
            axios.get(URL + LIST_AVAILABLE_BOTS_ENDPOINT).then(response => {
                bot.sendMessage(chatId, 'The bots available are the following: ' + response.data['bots']);
            })
            break;
        
        //If there are additional bots in the future, a '/set_bot' command would allow the user to select it's desired bot
        //case '/set_bot':
        //  break;


        //expense related message
        default:
            whitelisted = await isWhitelisted(userId);

            if (whitelisted) {
                //Set a bot instance
                await axios.post(URL + SET_BOT_ENDPOINT + '?bot_type=' + BOT_TYPE);

                axios.post(URL + PROCESS_MESSAGE_ENDPOINT + '?user_id=' + userId + '&message=' + '"' + msg.text + '"').then(response => {
                    bot.sendMessage(chatId, response.data[0]);
                })
            } else {
                bot.sendMessage(chatId, 'You are not whitelisted');
            }
            

    }
  
});
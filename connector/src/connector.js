const axios = require("axios");
const TelegramBot = require('node-telegram-bot-api');

if (process.env.PRODUCTION != true) {
    require('dotenv').config();
}


const token = process.env.TELEGRAM_BOT_API_KEY;
const BOT_TYPE = process.env.BOT_TYPE;
const bot = new TelegramBot(token, {polling: true});
const BOT_SERVICE_URL = process.env.BOT_SERVICE_URL
const IS_WHITELISTED_ENDPOINT = '/is_whitelisted';
const LIST_USER_EXPENSES_ENDPOINT = '/list_user_expenses';
const WHITELIST_USER_ENDPOINT = '/whitelist_user';
const SET_BOT_ENDPOINT = '/set_bot';
const LIST_AVAILABLE_BOTS_ENDPOINT = '/list_available_bots';
const PROCESS_MESSAGE_ENDPOINT = '/process_message';


async function isWhitelisted(userId) {
    const response =  await axios.get(BOT_SERVICE_URL + IS_WHITELISTED_ENDPOINT + '?user_id=' + userId);

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
            axios.post(BOT_SERVICE_URL + WHITELIST_USER_ENDPOINT + '?user_id=' + userId).then(response => {
                bot.sendMessage(chatId, response.data[0]);
            })

            break;
        
        //List all of a user's expenses
        case '/expenses':
            whitelisted = await isWhitelisted(userId);

            if (whitelisted) {
                axios.get(BOT_SERVICE_URL + LIST_USER_EXPENSES_ENDPOINT + '?user_id=' + userId).then(response => {
                    bot.sendMessage(chatId, printExpenses(response.data['expenses']));
                })
            } else {
                bot.sendMessage(chatId, 'You are not whitelisted');
            }

            break;

        //List all commands
        case '/help':
            help_msg = 
                '1) If not already whitelisted, type \\whitelitst to whitelist your user \n'+
                '2) Type a message with your expenses (e.g. "pizza 20 bucks") \n'+
                '3) Use the command \\expenses to list all your expenses \n'+

                'For a list of all available bots, type \\bots';
            bot.sendMessage(chatId, help_msg);
            break;
        
        //List all available bots
        case '/bots':
            axios.get(BOT_SERVICE_URL + LIST_AVAILABLE_BOTS_ENDPOINT).then(response => {
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
                await axios.post(BOT_SERVICE_URL + SET_BOT_ENDPOINT + '?bot_type=' + BOT_TYPE);

                axios.post(BOT_SERVICE_URL + PROCESS_MESSAGE_ENDPOINT + '?user_id=' + userId + '&message=' + '"' + msg.text + '"').then(response => {
                    bot.sendMessage(chatId, response.data[0]);
                })
            } else {
                bot.sendMessage(chatId, 'You are not whitelisted');
            }
            

    }
  
});


//Back4app requires that my app listens to a port, but that's not required for the telegram bot. So I listen on port 80 and do nothing.

const http = require('http');
const PORT = process.env.PORT || 80;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.end(); 
});

server.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
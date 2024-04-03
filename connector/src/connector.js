const express = require('express')
const expressApp = express()
const axios = require("axios");
expressApp.use(express.static('static'))
expressApp.use(express.json());
require('dotenv').config();

const TelegramBot = require('node-telegram-bot-api');

const token = process.env.TELEGRAM_BOT_API_KEY;
const bot = new TelegramBot(token, {polling: true});


function isWhitelisted(userId) {
    
}


bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    console.log("id: " + msg.from.id);
    switch (msg.text) {
        case '/expense':

            if (isWhitelisted(userId)) {
                axios.get(`https://darwinai-n3s5o067.b4a.run/list_user_expenses?user_id=1234`).then(response => {
                    bot.sendMessage(chatId, response.data[0]);
                })
            } else {
                bot.sendMessage(chatId, 'You are not whitelisted');
            }

            break;
        case '/help':
            bot.sendMessage(chatId, 'help');
            break;
        default:
            bot.sendMessage(chatId, 'Received your message');

    }
  
});


//bot.startPolling();
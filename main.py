#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import datetime
import telebot
import sqlite3 

API_TOKEN = '6077941896:AAFzfMFGMhBH10y8odpC2_wPl8nIkix-mb4'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    text =  message.text
    date = datetime.datetime.fromtimestamp(message.date)
    chat_id = message.chat.id
    user_id = message.from_user.id

    con = sqlite3.connect('history_db.db')
    with con:
        con.execute("INSERT INTO history (text, date, chat_id, user_id) VALUES (?, ?, ?, ?)", (text, date, chat_id, user_id))
        con.commit()
    bot.reply_to(message, message.text)


bot.infinity_polling()
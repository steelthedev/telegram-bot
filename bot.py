import logging
import threading
import json
import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler , Filters
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
from  scrape import *
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from telegram import KeyboardButton, ReplyKeyboardMarkup
from datetime import datetime
import pytz
import logging

bot_token = "1786157926:AAENP-1fUdw68NzRoV7z2wxJFNgsk0JnY50" #os.environ['steelbufferbot_token']
fauna_secret = "fnAEM72bnaACC-Yv5QYKHUyMm4rhRH6hwC5SdBOT" #os.environ['fauna_secret']
bot = telegram.Bot(token=bot_token)
fauna_secret = fauna_secret
client = FaunaClient(secret=fauna_secret)

import os
PORT = int(os.environ.get('PORT', 5000))

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def echo_thread(update, context):
    chat_id = update.effective_chat.id
    user = client.query(q.get(q.match(q.index("net_naija"), chat_id)))
    last_command = user["data"]["last_command"]

    if last_command == "search":
        title = update.message.text.strip()
        movie_list = SearchNetnaija(title)
        if len(movie_list) == 0:
            context.bot.send_message(chat_id=chat_id, text ="This movie isnt available , please check your wordings and try later")
        else:

            messages = ""

            title =  update.message.text.strip()

            for article in movie_list:
                movie_name = article["name"]

                try:

                    messages= f"\n {article['name']} \n {article['link']} \n\n {article['summary']}"
                    photo = article['image']
                    context.bot.send_photo(chat_id=chat_id, caption=messages , photo=photo)

                except:

                    pass
    else:
        context.bot.send_message(chat_id=chat_id, text = "You must enter the command /search ")









def start(update,context):
    chat_id = update.effective_chat.id
    first_name = update["message"]["chat"]["first_name"]
    username = update["message"]["chat"]["username"]

    try:
          user=client.query(q.get(q.match(q.index("net_naija"), chat_id)))
          client.query(q.update(q.ref(q.collection("buffer_bot"), user["ref"].id()), {"data": {"last_command": "start"}}))
          markup = ReplyKeyboardMarkup([[KeyboardButton("/search"), KeyboardButton("/latest"), KeyboardButton("/latest")] ], resize_keyboard=True)
          context.bot.send_message(chat_id=chat_id,text = f"Welcome BACK to STEEL BOT, {first_name}", reply_markup = markup)
    except:
        user = client.query(q.create(q.collection("buffer_bot"), {
            "data": {
                "id": chat_id,
                "first_name": first_name,
                "username": username,
                "last_command": "",
                "date": datetime.now(pytz.UTC)
            }
        }))
        client.query(q.update(q.ref(q.collection("buffer_bot"), user["ref"].id()), {"data": {"last_command": "start"}}))
        context.bot.send_message(chat_id=chat_id, text = f"Welcome to STEEL Bot, {first_name} . Your details have been saved 😊", reply_markup=markup)


def search(update, context):

    chat_id = update.effective_chat.id


    user = client.query(q.get(q.match(q.index("net_naija"), chat_id)))
    client.query(q.update(q.ref(q.collection("buffer_bot"), user["ref"].id()), {"data": {"last_command": "search"}}))

   
    context.bot.send_message(chat_id=chat_id, text ="Enter the name of your movie")





def echo(update, context):

    thread = threading.Thread(target= echo_thread, args=[update, context])

    thread.start()




def recommend(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(
        chat_id=chat_id, text=config["messages"]["recommend"])



updater=Updater("1786157926:AAENP-1fUdw68NzRoV7z2wxJFNgsk0JnY50",use_context=True)

dp=updater.dispatcher

dp.add_handler(CommandHandler("start",start))

dp.add_handler(CommandHandler("search", search) )

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dp.add_handler(echo_handler)

#updater.start_polling()

updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=bot_token)
updater.bot.setWebhook('https://steelbufferbot.herokuapp.com/' + bot_token)


updater.idle()

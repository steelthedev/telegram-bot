
import telegram
from telegram.ext import MessageHandler,CommandHandler,Updater, Filters
import threading
import logging
import json
import os
import time
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyMarkup
import datetime
import pymongo
from scrape import *


config = json.load(open("config.json"))

token = config["token"].format(os.environ['steelbufferbot_token'])

bot = telegram.Bot(token=token)

client = pymongo.MongoClient(config["db"]["host"], config["db"]["port"])

db = client[config["db"]["db_name"]]


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update,context):
    chat_id = update.effective_chat.id

    if not db.users.find_one({"chat_id":chat_id}):
        db.users.insert_one({"chat_id":chat_id, "admin":False, "mute":False, "last_command":None, "date":datetime.datetime.now()})
    db.users.update_one({"chat_id":chat_id},{"$set":{"active":True}})
    markup = ReplyKeyboardMarkup([[KeyboardButton("/search"), KeyboardButton("/get_latest"), KeyboardButton("/menu"), KeyboardButton("/search_kimoi")]], resize_keyboard=True)
    context.bot.send_message(chat_id, text = config["messages"]["welcome"].format(update["message"]["chat"]["first_name"]), parse_mode="Markdown", reply_markup=markup, disable_web_page_preview="True")
    db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":None}})


def search(update,context):
    chat_id = update.effective_chat.id
    last_command = "search"
    db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":last_command}})
    context.bot.send_message(chat_id, text=config["messages"]["search"])

def get_recent(update,context):
    chat_id = update.effective_chat.id
    last_command = "get_recent"
    db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":last_command}})

def menu(update,context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, text=config["messages"]["menu"])
    db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":None}})


def search_kimoi(update,context):
    chat_id = update.effective_chat.id
    last_command = "search_kimoi"
    db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":last_command}})
    context.bot.send_message(chat_id, text=config["messages"]["search"])

def echo(update,context):
    chat_id = update.effective_chat.id
    bot_user = db.users.find_one({"chat_id":chat_id})
    last_command = bot_user["last_command"] if bot_user != None else None

    if last_command == "search":
        title = update.message.text.strip()
        movie_list = SearchNetnaija(title)
        if len(movie_list) <= 0:
            context.bot.send_message(chat_id, text = "No result was found at this time.")
        else:
            [context.bot.send_photo(chat_id, caption=config["messages"]["search_result"].format(article["name"],article["link"],article["summary"]) , photo = article["image"])for article in movie_list]
        db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":None}})
    if last_command == "search_kimoi":
        title = update.message.text.strip()
        movie_list = SearchKimoi(title)
        if  len(movie_list) <= 0:
            context.bot.send_message(chat_id, text = "No result was found at this time.")
            print(movie_list)
        elif len(movie_list) > 0:
            [context.bot.send_message(chat_id, text=config["messages"]["kimoi_season"].format(season["season_name"],season["season_link"], season["season_name"]),parse_mode=telegram.ParseMode.HTML) for season in movie_list] 
        else:
            context.bot.send_message(chat_id, text = "No result was found at this time.")
        db.users.update_one({"chat_id":chat_id},{"$set":{"last_command":None}})
 
    

updater=Updater(token,use_context=True)

dp=updater.dispatcher


echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

dp.add_handler(CommandHandler("start",start))
dp.add_handler(CommandHandler("search",search))
dp.add_handler(CommandHandler("menu",menu))
dp.add_handler(CommandHandler("get_recent",get_recent))
dp.add_handler(CommandHandler("search_kimoi",search_kimoi))
dp.add_handler(echo_handler)

updater.start_polling()

updater.idle()
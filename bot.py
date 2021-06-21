import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler , Filters 
from telegram import  InlineKeyboardButton, InlineKeyboardMarkup
from  scrape import *


bot = telegram.Bot(token="1786157926:AAENP-1fUdw68NzRoV7z2wxJFNgsk0JnY50")

def start(update,context):
    
    content = scraperecent()

    for article in content:
        try:
            update.message.reply_text(f"{article['image']} {article['name']}, {article['href']}")
           
        except:
            pass

    

def new(update, context):
    update.message.reply_text("Hold on for something new")

def main():
    updater=Updater("1786157926:AAENP-1fUdw68NzRoV7z2wxJFNgsk0JnY50",use_context=True)

    dp=updater.dispatcher

    dp.add_handler(CommandHandler("start",start))
    dp.add_handler(CommandHandler("new",new))

    updater.start_polling()

    updater.idle()
if __name__ == '__main__':
    main()

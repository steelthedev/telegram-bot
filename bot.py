import logging
from telegram.ext import Updater, CommandHandler , MessageHandler , Filters 
from  scrape import *

def start(update, context):
    
    update.message.reply_text(article_name)

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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
This Bot uses the Updater class to handle the bot.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import glob, os, sys, time
from youtube import Download
from mutagen.mp4 import MP4
from pprint import pprint
import urllib.parse as urlparse
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler("tplayer.log")
stream_handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text('Hi!')


def help(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    logger.info(dir(update))
    sent_message = update.message.reply_text('try to download {0}'.format(update.message.text))
    user = update.message.from_user
    logger.info("Request {3} from chat_id:{4} first_name:{0} ,last_name:{1} ,username:{2}"
            .format(user.first_name,user.last_name,user.username,update.message.text,update.message.chat_id
))
    chat_id = update.message.chat_id
    try:
        d = Download()
        parsed = update.message.text.split("&list=")[0]
        infodict = d.download(parsed)
        file = glob.glob('./mp3/*{0}.m4a'.format(infodict['display_id']))
        print (file)
        audio = MP4(file[0])
        audio["\xa9nam"] = infodict['title']
        audio["\xa9ART"] = infodict['uploader']
        audio.save()
        bot.edit_message_text(f'{infodict["title"]} downloaded',chat_id=chat_id,message_id=sent_message.message_id)
        # bot.send_document(chat_id=chat_id, document=open(file[0], 'rb'),timeout=200)
        bot.send_audio(chat_id=chat_id, audio=open(file[0], 'rb'),timeout=2000,title=infodict['title'])
    except Exception as e:
        logger.error(e)
        update.message.reply_text('System error'+str(e))



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(os.environ['TOKEN'])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler((Filters.text), echo))
    # dp.add_handler(MessageHandler((Filters.text & Filters.private), echo))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    logging.info('TPlayer started')
    main()

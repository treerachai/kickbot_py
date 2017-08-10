#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import *
import csv, sys, time

forbiddenWords = []
group_admin = []

def importCSV():
    # with open('/home/pi/kickbot_py/forbiddenWords.csv', 'rb') as f:
    with open('forbiddenWords.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            forbiddenWords.extend(row)
        print(forbiddenWords)
    f.close()


def appendCSV(word):
    word.lower()
    # check if word is barely legal
    for fw in forbiddenWords:
        if fw == word:
            return False
    # with open('/home/pi/kickbot_py/forbiddenWords.csv', 'a') as f:
    with open('forbiddenWords.csv', 'a') as f:
        f.write(word + "\r\n")
    f.close()
    forbiddenWords.extend(word)
    print("Word %s added!", word)
    return True


def snforbidden(bot, update):
    user = update.message.from_user
    if user.name not in group_admin:
        update.message.reply_text("La aggiungo solo se te lo meriti")
    else:
        update.message.reply_text("Uhuh! Delizioso!")
        sendedText = update.message.text.split()
        if len(sendedText) > 1:
            for word in sendedText[1:]:
                appendCSV(word)

def start(bot, update):
    get_admin_ids(bot.get_chat_administrators(update.message.chat_id))
    update.message.reply_text("Il gioco è appena iniziato.")

def help(bot, update):
    update.message.reply_text("Qualche parola ti farà bannare, molte altre no :) .")

def get_admin_ids(admin_obj):
    global group_admin
    admins = ([admin.user.name for admin in admin_obj])
    if not group_admin:
        group_admin = admins
    # print(group_admin)

def checkMessage(bot, update):
    # global group_admin
    # print(update.message.text) 			# take text message
    # print(update.message.chat_id) 		# take chat id
    # print(update.message.from_user.id) 	# take user id
    user_message = update.message.text.lower()
    user = update.message.from_user
    for word in forbiddenWords:
        print(word)
        if word in user_message:
            # print(bot.get_chat_administrators(update.message.chat_id));
            update.message.reply_text("Whops! Cosa abbiamo qui?")
            # print("test passato")
            # print(user.name)
            # print(group_admin)
            if user.name in group_admin:
                bot.send_message(update.message.chat_id, "Facile "+user.name+" quando sei admin")
                return False
            time.sleep(0.5)
            bot.send_message(update.message.chat_id, "Ehi "+user.name+" pensavi di farla franca eh?")
            time.sleep(0.5)
            bot.send_message(update.message.chat_id, "e io ti banno")
            time.sleep(0.8)
            bot.send_message(update.message.chat_id, "avoglia se ti banno")
            bot.kickChatMember(update.message.chat_id, user.id)
            bot.unbanChatMember(update.message.chat_id, user.id)
            bot.send_message(update.message.chat_id, "ecco fatto :D")
            time.sleep(0.3)
            bot.send_message(update.message.chat_id, "IL PROSSIMO!")

def main():
    importCSV()
    updater = Updater("352628614:AAGd9OPwCmUeVeEISFjKHs4si95-57mv-ro")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("snforbidden", snforbidden))
    dp.add_handler(MessageHandler(Filters.text, checkMessage))
    updater.start_polling()
    try:
        print("Ready")
        updater.idle()
    except KeyboardInterrupt:
        print("questo print non funziona")


if __name__ == '__main__':
    main()

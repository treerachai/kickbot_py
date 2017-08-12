#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: se non è stato eseguito start almeno la prima volta, non far funzionare niente altro
from telegram.ext import *

import csv, sys, time, os.path

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
    if len(word) < 3: 
        return False
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

 # TODO: modificare il codice aggiungendo questa funzione per le opzioni solo per admin
def isAdmin(user, admin_obj):
    if user in get_admin_ids(admin_obj):
        return True
    return False


 # TODO: finire la funzione update_admin gestire l'aggiornamento vedi commeento
 # TODO: aggiorna il codice dove usi questa funzione
def update_admin(chat_id, admin_obj, me):
    admin = get_admin_ids(admin_obj)
    filepath = "res/"+str(chat_id)+"/members.csv"
    if not os.path.exists(filepath):
        with open(filepath, 'wb') as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["member_nick", "admin", "kick_times"])
            admin.remove("@"+me.username)
            for user in admin:
                wr.writerow([user, 1, 0])
            file.close()
    else:
        # questo
        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            print(reader)
            for row in reader:
                print(row)
    print(admin)
    return admin

def snforbidden(bot, update):
    user = update.message.from_user
    if not isAdmin(user.name, bot.get_chat_administrators(update.message.chat_id)):
        update.message.reply_text("La aggiungo solo se te lo meriti")
    else:
        update.message.reply_text("Uhuh! Delizioso!")
        sendedText = update.message.text.split()
        if len(sendedText) > 1:
            for word in sendedText[1:]:
                if not appendCSV(word):
                    bot.send_message(update.message.chat_id, "peccato che qualcuno abbia pensato a " + word + " prima di te")

def start(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    config_path = "res/"+str(chat_id)
    print(config_path)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
    if not os.path.exists(config_path+"/config.csv"):
        with open(config_path+"/config.csv", 'wb') as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["property", "value"])
            wr.writerow(["ready", "true"])
            file.close()
    admin = update_admin(update.message.chat_id, bot.get_chat_administrators(update.message.chat_id), bot.getMe())
        # with open(config_path+"/members.csv  ", 'wb') as file:
        #     wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_ALL)
        #     wr.writerow(["member_nick", "admin", "kick_times"])
        #     admin = get_admin_ids(bot.get_chat_administrators(update.message.chat_id))
        #     admin.remove("@"+bot.getMe().username)
        #     for user in admin:
        #         wr.writerow([user, 1, 0])
        #     file.close()

    update.message.reply_text("Il gioco è appena iniziato.")

def test(bot, update):
    print(True)

def help(bot, update):
    update.message.reply_text("Qualche parola ti farà bannare, molte altre no :)")
    bot.send_message(update.message.chat_id, "si consiglia di aggiungere il bot agli admin prima di eseguire il comando /start")

def get_admin_ids(admin_obj):
    admins = ([admin.user.name for admin in admin_obj])
    print(admins)
    return admins
    # if not group_admin:
    #     group_admin = admins
    # print(group_admin)

def checkMessage(bot, update):
    # print(update.message.text) 			# take text message
    # print(update.message.chat_id) 		# take chat id
    # print(update.message.from_user.id) 	# take user id
    user_message = update.message.text.lower()
    user = update.message.from_user
    for word in forbiddenWords:
        # print(word)
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
    dp.add_handler(CommandHandler("test", test))
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

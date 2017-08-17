#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: se non è stato eseguito start almeno la prima volta, non far funzionare niente altro
from telegram.ext import *

import csv, sys, time, os.path, pandas


def forbiddenWords(chat_id):
    if os.path.exists("res/" + str(chat_id) + "/forbidden_words.csv"):
        ret_forbidden = []
        with open("res/" + str(chat_id) + "/forbidden_words.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                ret_forbidden.extend(row)
        f.close()
    else:
        return False
    return ret_forbidden


def appendCSV(word, chat_id):
    word.lower()
    # check if word is barely legal
    if len(word) < 3:
        return False
    for fw in forbiddenWords(chat_id):
        if fw == word:
            return False
    # with open('/home/pi/kickbot_py/forbiddenWords.csv', 'a') as f:
    with open('res/' + str(chat_id) + '/forbidden_words.csv', 'a') as f:
        wr = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONE)
        wr.writerow([word])
        f.close()
    print("Word %s added!", word)
    return True


def isAdmin(user, admin_obj):
    if user in get_admin_ids(admin_obj):
        return True
    return False


def manageUser(user, chat_id):
    user_file = []
    with open('res/' + str(chat_id) + '/users.csv', 'r') as f:
        print('wow')
        reader = csv.reader(f)
        for row in reader:
            user_file.extend([row[0].split(";")])
        f.close()
        # print(user_file)
    print(user_file)
    for row in user_file:
        # print(row[0])
        # print(user)
        # print(user == row[0])
        # print(str(user) == row[0])
        if str(user) in row[0]:
            print('wow2')
            f = pandas.read_csv('res/' + str(chat_id) + '/users.csv', sep=';')
            f1 = f.set_index("user_id")
            print(f1)
            print(f1.get_value(user, "kicked"))
            # print(f1.get_value(user, "user_id"))
            # print(f.loc[str(user)])
            # print(f[f['user_id'] == str(user)].index[0])
            k_times = f1.get_value(user, "kicked")+1
            print(k_times)
            f1.set_value(user, "kicked", k_times)
            print('passed')
            #TOD(ieg)O: questa istruzione non sovrsrive il file
            f1.to_csv(path_or_buf='res/' + chat_id + '/users.csv', sep=';')
            return True

    with open('res/' + str(chat_id) + '/users.csv', 'a') as f:
        wr = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONE)
        wr.writerow([user, 1])
        f.close()


def snforbidden(bot, update):
    user = update.message.from_user
    if not isAdmin(user.id, bot.get_chat_administrators(update.message.chat_id)):
        update.message.reply_text("La aggiungo solo se te lo meriti")
    else:
        update.message.reply_text("Uhuh! Delizioso!")
        sendedText = update.message.text.split()
        if len(sendedText) > 1:
            for word in sendedText[1:]:
                if not appendCSV(word, update.message.chat_id):
                    bot.send_message(update.message.chat_id,"peccato che qualcuno abbia pensato a " + word + " prima di te")


def start(bot, update):
    chat_id = update.message.chat_id
    print(chat_id)
    config_path = "res/" + str(chat_id)
    print(config_path)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        with open(config_path + "/config.csv", 'wb') as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["property", "value"])
            wr.writerow(["ready", "true"])
            file.close()
        with open(config_path + "/forbidden_words.csv", "wb") as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["catafalco"])
            file.close()
        with open(config_path + '/users.csv', 'wb') as f:
            wr = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["user_id", "kicked"])
            f.close()

    update.message.reply_text("Il gioco è appena iniziato.")


def test(bot, update):
    print(forbiddenWords(update.message.chat_id))


def help(bot, update):
    update.message.reply_text("Qualche parola ti farà bannare, molte altre no :)")
    bot.send_message(update.message.chat_id,
                     "si consiglia di aggiungere il bot agli admin prima di eseguire il comando /start")


def get_admin_ids(admin_obj):
    admins = ([admin.user.id for admin in admin_obj])
    # print(admins)
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
    # print(user_message)
    # print(forbiddenWords)
    for word in forbiddenWords(update.message.chat_id):
        # print(word)
        if word in user_message:
            # print(bot.get_chat_administrators(update.message.chat_id));
            update.message.reply_text("Whops! Cosa abbiamo qui?")
            manageUser(user.id, update.message.chat_id)
            # print("test passato")
            # print(user.name)
            # print(group_admin)
            if isAdmin(user.id, bot.get_chat_administrators(update.message.chat_id)):
                bot.send_message(update.message.chat_id, "Facile " + user.name + " quando sei admin")
                return False
            time.sleep(1)
            bot.send_message(update.message.chat_id, "Ehi " + user.name + " pensavi di farla franca eh?")
            time.sleep(1)
            bot.send_message(update.message.chat_id, "e io ti banno")
            time.sleep(1)
            bot.send_message(update.message.chat_id, "avoglia se ti banno")
            if update.message.from_user.id == 111612345 or update.message.from_user.id == 17232977:
                bot.send_message(update.message.chat_id, 'ma io non posso bannare il mio papà')
                return False
            bot.kickChatMember(update.message.chat_id, user.id)
            if update.message.chat.type == "supergroup":
                bot.unbanChatMember(update.message.chat_id, user.id)
            bot.send_message(update.message.chat_id, "ecco fatto :D")
            bot.send_message(update.message.chat_id, "IL PROSSIMO!")


def main():
    #    importCSV()
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

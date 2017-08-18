#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram.ext import *
from emoji import emojize
import csv, sys, time, os.path, pandas, telegram


def forbiddenWords(chat_id):
    if os.path.exists("res/" + str(chat_id) + "/forbidden_words.csv"):
        ret_forbidden = []
        f = pandas.read_csv('res/' + str(chat_id) + '/forbidden_words.csv', sep=';')
        for row in f.values:
            ret_forbidden.append(row[0])
            # with open("res/" + str(chat_id) + "/forbidden_words.csv", "r") as f:
            #     reader = csv.reader(f)
            #     for row in reader:
            #         ret_forbidden.extend(row)
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
        wr.writerow([word, 0])
        f.close()
    print("Word %s added!", word)
    return True


def isAdmin(user, admin_obj):
    if user.id in get_admin_ids(admin_obj):
        return True
    return False


def addUser(user, chat_id):
    f = pandas.read_csv('res/' + str(chat_id) + '/users.csv', sep=';')
    f1 = f.set_index("user_id")
    if user.id not in f1.index.values:
        new_df = pandas.DataFrame([[user.id, user.name, 0]], columns=['user_id', 'user_name', 'kicked'])
        f = pandas.DataFrame(f)
        f = f.append(new_df)
        f.to_csv('res/' + str(chat_id) + '/users.csv', sep=';', index=False)
        return True
    return False


def manageUser(user, chat_id):
    f = pandas.read_csv('res/' + str(chat_id) + '/users.csv', sep=';')
    f1 = f.set_index("user_id")
    k_times = f1.get_value(user.id, "kicked") + 1
    f1.set_value(user.id, "kicked", k_times)
    f1.to_csv('res/' + str(chat_id) + '/users.csv', sep=';')
    return True


def countWord(word, chat_id):
    print('start countWord')
    f = pandas.read_csv('res/' + str(chat_id) + '/forbidden_words.csv', sep=';')
    f_index = f.set_index('word')
    k_times = f_index.get_value(word, 'called_times') + 1
    f_index.set_value(word, 'called_times', k_times)
    f_index.to_csv('res/' + str(chat_id) + '/forbidden_words.csv', sep=';')


def snforbidden(bot, update):
    user = update.message.from_user
    if not isAdmin(user, bot.get_chat_administrators(
            update.message.chat_id)) and not ( update.message.from_user.id == 111612345 or update.message.from_user.id == 17232977):
        update.message.reply_text("La aggiungo solo se te lo meriti")
    else:
        update.message.reply_text("Uhuh! Delizioso!")
        sendedText = update.message.text.split()
        if len(sendedText) > 1:
            for word in sendedText[1:]:
                if not appendCSV(word, update.message.chat_id):
                    bot.send_message(update.message.chat_id,
                                     "peccato che qualcuno abbia pensato a " + word + " prima di te")


def stat(bot, update):
    chat_id = update.message.chat_id
    pos = 1
    f = pandas.read_csv('res/' + str(chat_id) + '/users.csv', sep=';')
    message = ':tada: LA CLASSIFICA :tada:\r\nqui potrete vedere l\'attuale campione di KickBot e tutti i fancazzisti del canale che si cimentano alla ricerca delle parole vietate per poi farsi kickare in malo modo\r\n'
    sorted_f = pandas.DataFrame(f)
    sorted_f = sorted_f.sort_values(['kicked'], ascending=False)
    for user in sorted_f.values:
        # message.add_row([pos, user[1].split('@')[1], user[2]])
        if pos == 1:
            message = message + ":1st_place_medal:" + user[1] + " :arrow_backward:" + str(user[2])
        elif pos == 2:
            message = message + ":2nd_place_medal:" + user[1] + " :arrow_backward:" + str(user[2])
        elif pos == 3:
            message = message + ":3rd_place_medal:" + user[1] + " :arrow_backward:" + str(user[2])
        else:
            message = message + str(pos) + " " + user[1].split('@')[1].capitalize() + ":arrow_backward:" + str(user[2])

        if user[2] == 1:
            message = message + " volta\r\n"
        else:
            message = message + " volte\r\n"
        pos = pos + 1
    message = message + "\r\n most used word:\r\n"
    forbidden_f = pandas.read_csv('res/' + str(chat_id) + '/forbidden_words.csv', sep=';')
    sorted_words = pandas.DataFrame(forbidden_f)
    sorted_words = sorted_words.sort_values(['called_times'], ascending=False)
    message = message + '<b>' + sorted_words.values[0][0].upper() + '</b> usata ben: ' + str(sorted_words.values[0][1])
    if sorted_words.values[0][1] == 1:
        message = message + ' volta'
    else:
        message = message + ' volte'

    bot.send_message(chat_id=chat_id, text=emojize(message, use_aliases=True), parse_mode=telegram.ParseMode.HTML)


def start(bot, update):
    chat_id = update.message.chat_id
    config_path = "res/" + str(chat_id)
    if not os.path.exists(config_path):
        os.makedirs(config_path)
        with open(config_path + "/config.csv", 'wb') as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["property", "value"])
            wr.writerow(["ready", "true"])
            wr.writerow(["group_name", update.message.chat.title])
            file.close()
        with open(config_path + "/forbidden_words.csv", "wb") as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["word", "called_times"])
            wr.writerow(["catafalco", 0])
            file.close()
        with open(config_path + '/users.csv', 'wb') as f:
            wr = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["user_id", "user_name", "kicked"])
            f.close()
        update.message.reply_text("Il gioco è appena iniziato.")
    else:
        if not os.path.exists(config_path + "/config.csv"):
            with open(config_path + "/config.csv", 'wb') as file:
                wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
                wr.writerow(["property", "value"])
                wr.writerow(["ready", "true"])
                wr.writerow(["group_name", update.message.chat.title])
                file.close()
    if not os.path.exists(config_path + "/forbidden_words.csv"):
        with open(config_path + "/forbidden_words.csv", "wb") as file:
            wr = csv.writer(file, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["word", "called_times"])
            wr.writerow(["catafalco", 0])
            file.close()
    if not os.path.exists(config_path + "/users.csv"):
        with open(config_path + '/users.csv', 'wb') as f:
            wr = csv.writer(f, delimiter=";", quoting=csv.QUOTE_NONE)
            wr.writerow(["user_id", "user_name", "kicked"])
            f.close()
    update.message.reply_text("Il gioco è già iniziato.")


def my_id(bot, update):
    bot.send_message(update.message.chat_id, update.message.from_user.id)


def test(bot, update):
    print(update.message.chat)


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
    print(update.message.chat_id)
    addUser(user, update.message.chat_id)
    for word in forbiddenWords(update.message.chat_id):
        if word in user_message:
            # print(bot.get_chat_administrators(update.message.chat_id));
            update.message.reply_text("Whops! Cosa abbiamo qui?")
            countWord(word, update.message.chat_id)
            manageUser(user, update.message.chat_id)
            # print("test passato")
            # print(user.name)
            # print(group_admin)
            if isAdmin(user, bot.get_chat_administrators(update.message.chat_id)):
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
    dp.add_handler(CommandHandler("id", my_id))
    dp.add_handler(CommandHandler("stat", stat))
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

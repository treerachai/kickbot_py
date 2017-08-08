#!/usr/bin/env python
#-*- coding: utf-8 -*-

from telegram.ext import *
import csv,sys

forbiddenWords = []

def importCSV():
	with open('forbiddenWords.csv','rb') as f:
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
	with open('forbiddenWords.csv','w') as f:
		f.write(word)
#	f=open('forbiddenWords.csv','w')
#	writer=csv.writer(f,delimiter='',quotechar="",quoting=csv.QUOTE_ALL)
#	writer.writerow(word)
	f.close()
	forbiddenWords.extend(word)
	print("Word %s added!",word)
	return True

def snforbidden(bot,update):
	update.message.reply_text("Uhuh! Delizioso!")
	sendedText=update.message.text.split()
	if len(sendedText) > 1:
		for word in sendedText[1:]:
			appendCSV(word)

def start(bot,update):
	update.message.reply_text("Il gioco è già iniziato.")

def help(bot,update):
	update.message.reply_text("Qualche parola ti farà bannare, molte altre no :) .")

def function(bot,update):
	# update.message.reply_text(update.message.text)
	# print(update.message.text) 			# take text message
	# print(update.message.chat_id) 		# take chat id
	# print(update.message.from_user.id) 		# take user id
	user_message = update.message.text.lower()
	for word in forbiddenWords:
		if word in user_message:
			update.message.reply_text("Whops! Cosa abbiamo qui?")
			if bot.kickChatMember(update.message.chat_id,update.message.from_user.id):
				bot.unbanChatMember(update.message.chat_id,update.message.from_user.id)
				break
			else:
				update.message.reply_text("Troppo facile senza che io sia admin.")

def main():
	importCSV()
	updater = Updater("352628614:AAGd9OPwCmUeVeEISFjKHs4si95-57mv-ro")
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help",help))
	dp.add_handler(CommandHandler("snforbidden",snforbidden))
	dp.add_handler(MessageHandler(Filters.text,function))
	updater.start_polling()
	try:
		print("Ready")
		updater.idle()
	except KeyboardInterrupt:
		print("questo print non funziona")

if __name__ == '__main__':
    main()

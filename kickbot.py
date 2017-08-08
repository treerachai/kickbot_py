#!/usr/bin/env python

from telegram.ext import *

forbiddenWords = ['rododendro','mirtillo','pneumatico','falange','stuzzicante']

def start(bot,update):
	update.message.reply_text("Il gioco e gia iniziato.")

def help(bot,update):
	update.message.reply_text("Qualche parola ti fara bannare, molte altre no :smile: .")

def function(bot,update):
	# update.message.reply_text(update.message.text)
	# print(update.message.text) 			# take text message
	# print(update.message.chat_id) 		# take chat id 
	# print(update.message.from_user.id) 	# take user id
	user_message = update.message.text
	for word in forbiddenWords:
		if word in user_message:
			if bot.kickChatMember(update.message.chat_id,update.message.from_user.id):
				bot.unbanChatMember(update.message.chat_id,update.message.from_user.id)
				break
			else:
				print("Fammi admin dio cane!")

def main():
	updater = Updater("352628614:AAGd9OPwCmUeVeEISFjKHs4si95-57mv-ro")
	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start",start))
	dp.add_handler(CommandHandler("help",help))
	dp.add_handler(MessageHandler(Filters.text,function))
	updater.start_polling()
	try:
		print("Ready")
		updater.idle()
	except KeyboardInterrupt: 
		print("diocaneeeeeeeeee")

if __name__ == '__main__':
    main()
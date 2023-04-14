import telepot

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text':
        cmd = msg['text'].split()
        print cmd
        if cmd[0] == '/start':
            bot.sendMessage(chat_id, "ciao, benvenuto nella mia chat!")
        elif cmd[0] == '/ciao':
            bot.sendMessage(chat_id, "ciao, come stai?")
		
TOKEN = '6157401708:AAFLqxZTjeAFg_N3Su7GnNxOqQKEJoIi_aE'

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)

print 'Listening ...'

import time
while 1:
    time.sleep(10)
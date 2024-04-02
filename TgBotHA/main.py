#loading config
import json
addon_config = None
with open('/data/options.json', 'r') as file:
    addon_config = json.load(file)

group_id = addon_config['group_id'] or 0
bot_id = addon_config['bot_id'] or ""
webhook_id_1 = addon_config['webhook_id_1'] or ""
webhook_id_2 = addon_config['webhook_id_2'] or ""
webhook_lights_on = 'http://homeassistant:8123/api/webhook/' + webhook_id_1
webhook_lights_off = 'http://homeassistant:8123/api/webhook/' + webhook_id_2
admin_id = addon_config['admin_id'] or 0
admins =[]
admins.append(admin_id)

if bot_id == "":
    raise ValueError("Error: No Bot ID supplied")
if webhook_id_1 == "":
    raise ValueError("Error: No Webhook 1 ID supplied")
if webhook_id_2 == "":
    raise ValueError("Error: No Webhook 2 ID supplied")
if admin_id == 0:
    raise ValueError("Error: No Admin ID supplied")

import telebot
from telebot import types

bot = telebot.TeleBot(bot_id)

markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Lights On')
itembtn2 = types.KeyboardButton('Lights Off')
markup.add(itembtn1)
markup.add(itembtn2)
markup_remove = types.ReplyKeyboardRemove(selective=False)

import requests

print("The Bot is running")

@bot.message_handler()
def user_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    
    if user_id not in admins:
        # print(f"user outside of group - id:' {user_id} name: {message.from_user.first_name} {message.from_user.last_name}")
        bot.send_message(chat_id,':)')
        return
    
    elif text == 'Lights On':
        bot.send_message(chat_id, f'<b>Turning Lights On!</b>', parse_mode='html')
        myobj = {'somekey': 'somevalue'}
        x = requests.post(webhook_lights_on, json = myobj)
    elif text == 'Lights Off':
        bot.send_message(chat_id, f'<b>Turning Lights Off!</b>', parse_mode='html')
        myobj = {'somekey': 'somevalue'}
        x = requests.post(webhook_lights_off, json = myobj)
        
    else:
        bot.send_message(chat_id,'Press button for Lights',reply_markup=markup)

bot.polling(none_stop=True)
print("Bot has stopped")
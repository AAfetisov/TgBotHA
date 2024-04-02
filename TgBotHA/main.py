import json
import telebot
import requests
from telebot import types

# Constants
DEFAULT_ADMIN_ID = 0
HOME_ASSISTANT_API_URL = 'http://homeassistant:8123/api/webhook/'

# Load configuration
with open('/data/options.json', 'r') as file:
    addon_config = json.load(file)

# Check configuration
required_keys = ['bot_id', 'webhook_id_1', 'webhook_id_2', 'admin_id']
for key in required_keys:
    if key not in addon_config or not addon_config[key]:
        raise ValueError(f"Error: {key} not found or empty in configuration")

group_id = addon_config['group_id']
bot_id = addon_config['bot_id']
webhook_id_1 = addon_config['webhook_id_1']
webhook_id_2 = addon_config['webhook_id_2']
webhook_lights_on = HOME_ASSISTANT_API_URL + webhook_id_1
webhook_lights_off = HOME_ASSISTANT_API_URL + webhook_id_2
admin_id = addon_config['admin_id']
admins = [admin_id]

# Initialize bot
bot = telebot.TeleBot(bot_id)

# Initialize markup
markup = types.ReplyKeyboardMarkup(row_width=2)
itembtn1 = types.KeyboardButton('Lights On')
itembtn2 = types.KeyboardButton('Lights Off')
markup.add(itembtn1, itembtn2)
markup_remove = types.ReplyKeyboardRemove(selective=False)

@bot.message_handler()
def user_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text
    myobj = {'somekey': 'somevalue'}

    if user_id not in admins:
        bot.send_message(chat_id,':)')
        return
    
    elif text == 'Lights On':
        bot.send_message(chat_id, f'<b>Turning Lights On!</b>', parse_mode='html')
        
        x = requests.post(webhook_lights_on, json = myobj)
    elif text == 'Lights Off':
        bot.send_message(chat_id, f'<b>Turning Lights Off!</b>', parse_mode='html')
        x = requests.post(webhook_lights_off, json = myobj)
        
    else:
        bot.send_message(chat_id,'Press button for Lights',reply_markup=markup)

print("The Bot is running")
bot.polling(none_stop=True)
print("Bot has stopped")
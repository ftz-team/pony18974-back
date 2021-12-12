import telebot
from time import sleep


BOT_TOKEN = '5019796180:AAHS0Ctq0_IHFdpr4_0eUya6gKKz-OvUMcY'
CHANNEL_NAME = '@wash_notify'

bot = telebot.TeleBot(BOT_TOKEN)

def send_message(instance):
    slot = instance.slot.time_range
    code = instance.code

    msg = f'Новая запись на {slot}! \nКод записи - {code}'
    bot.send_message(CHANNEL_NAME, msg)
    sleep(1)

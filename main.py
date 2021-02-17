import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import calendar
import asyncio

templates = {
    "/ping": {
        "en": "Hello",
        "uk": "Привіт",
        "ru": "Привет"
    }
}

operation_stack = []

bot = telebot.TeleBot("1598131905:AAHet6HGCkuD6zYcN3AVzVovWqR2PPlWBZY")


async def stack_reducer():
    while True:
        for i in operation_stack:
            if time.time() >= i["timestamp"]:
                i["operation"]()
                operation_stack.remove(i)

def form_message(msg_meta):
    data = f"{templates['greatings'][msg_meta['from']['language_code']]}," \
           f" {msg_meta['from']['first_name']} {msg_meta['from']['last_name']}!"
    return data


def form_ping_message(msg_meta):
    data = f"request_type: ping\n" \
           f"data_content: {msg_meta['text']}\n" \
           f"from: @{msg_meta['from']['username']}\n" \
           f"timestamp: {msg_meta['date']}\n" \
           f"language_code: {msg_meta['from']['language_code']}"
    return data


def make_remind(msg_meta):
    pass


def make_remind_to_someone():
    pass


@bot.message_handler(commands=['ping', 'help'])
def ping(message):
    formed_message = form_ping_message(message.json)
    bot.send_message(message.chat.id, formed_message)


# @bot.message_handler(func=lambda message: True)
# def echo_all(message):
#     bot.reply_to(message, message.text)

def gen_calendar():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(commands=['calendar', 'help'])
def call_calendar(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_calendar())



# asyncio.run(stack_reducer())
bot.polling()
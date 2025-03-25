import telebot
from telebot import types
import time

global block
block = 0
global blck


# Токен вашего бота (замените на свой)
TOKEN = '7587992589:AAFPtTAk2QlRgmuRw85YVbuw4DML2d70_GE'
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения вопросов пользователей (можно заменить на БД)
user_questions = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):

    

    global user_id
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📞 Сдать номер")
    markup.add(btn1)
    
    bot.send_message(
        message.chat.id,
        "👋 Привет! Это бот сдачи номеров ватсап.\n"
        "Выберите действие:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "📞 Сдать номер")
def contact_support(message):


    markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        "✍️ Напишите номер, когда его возьмут вам придет умедовление:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, save_question)

def save_question(message):
    user_questions[message.chat.id] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("✅ Да")
    btn2 = types.KeyboardButton("❌ Нет")
    markup.add(btn1, btn2)
    
    bot.send_message(
        message.chat.id,
        f"Ваш номер: *{message.text}*\n\nВсё верно?",
        reply_markup=markup,
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, confirm_question)

def confirm_question(message):
    if message.text == "✅ Да":
        bot.send_message(
            message.chat.id,
            "✅ Ваш номер отправлен! Ожидайте ответа.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        
        # Здесь можно добавить логику отправки вопроса админу
        global admin_chat_id
        admin_chat_id = "7783847586"  # Замените на ID админа
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Взять", callback_data=f"reply_{message.chat.id}_{message.message_id}")
        btn1 = types.InlineKeyboardButton("Отправить код", callback_data=f"code{message.chat.id}_{message.message_id}")
        btn2 = types.InlineKeyboardButton("Выстоял", callback_data=f"sucessfully{message.chat.id}_{message.message_id}")
        btn3 = types.InlineKeyboardButton("Выслать оплату", callback_data=f"oplatit{message.chat.id}_{message.message_id}")
        markup.add(btn, btn1, btn2, btn3)
        bot.send_message(
            admin_chat_id,
            f"Новый номер от пользователя. {message.chat.id}:\n\n{user_questions[message.chat.id]}", reply_markup=markup
        )

        bot.register_next_step_handler(message, save_question)


@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def handle_button_click(call):
    code(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("code"))
def handle_button_click(call):
    save_answer(call.message)
@bot.callback_query_handler(func=lambda call: call.data.startswith("sucessfully"))
def handle_button_click(call):
    sucessful(call.message)

@bot.callback_query_handler(func=lambda call: call.data.startswith("oplatit"))
def handle_button_click(call):
    oplata(call.message)

def oplata(message):
    bot.send_message(admin_chat_id, "Отправьте ссылку на чек:")
    bot.register_next_step_handler(message, check)

def check(message):
    c = message.text
    bot.send_message(user_id, f"Ваша оплата: {c}")
def sucessful(message):
    bot.send_message(admin_chat_id, f"Вы подали информацию дропу с номером {user_questions} о том, что он выстоял. Не забудьте выслать оплату.")
    bot.send_message(user_id, f"Ваш номер выстоял! Ожидайте оплату.")

def code(message):
    bot.send_message(admin_chat_id, f"Номер {user_questions} взят! (Дропу отправленно сообщение)")
    bot.send_message(user_id, f"Ваш номер взят! ожидайте код!")

def save_answer(message):
    bot.send_message(admin_chat_id, "Отправьте код:")
    bot.register_next_step_handler(message, hser)

def hser(message):
    x = message.text
    bot.send_message(user_id, f"Код:{x}")


    


bot.polling(non_stop=True)
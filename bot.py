import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 1203563417

bot = telebot.TeleBot(TOKEN)
user_waiting_for_screenshot = set()

# Временное хранилище для скриншотов
pending_screenshots = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Бот запущен. Отправь /pay, чтобы начать оплату.")

@bot.message_handler(commands=['pay'])
def pay(message):
    chat_id = message.chat.id
    user_waiting_for_screenshot.add(chat_id)
    bot.send_message(chat_id, "Отправьте скриншот оплаты.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    print(f"📸 Получено фото от {chat_id}")

    if chat_id == ADMIN_ID:
        bot.reply_to(message, f"File ID: {message.photo[-1].file_id}")
        return

    if chat_id in user_waiting_for_screenshot:
        # Сохраняем file_id
        file_id = message.photo[-1].file_id
        pending_screenshots[chat_id] = file_id
        
        # Создаём кнопки для админа
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("✅ Подтвердить", callback_data=f"approve_{chat_id}"),
            types.InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{chat_id}")
        )
        
        # Отправляем админу
        bot.send_photo(
            ADMIN_ID,
            file_id,
            caption=f"Скриншот от пользователя {chat_id}",
            reply_markup=markup
        )
        
        bot.send_message(chat_id, "Скриншот отправлен админу.")
        user_waiting_for_screenshot.remove(chat_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    print(f"🔘 Нажата кнопка: {call.data}")
    
    if call.data.startswith("approve_"):
        user_id = int(call.data.split("_")[1])
        bot.send_message(user_id, "✅ Оплата подтверждена! Вот ваш гайд.")
        bot.answer_callback_query(call.id, "Гайд отправлен!")
        
    elif call.data.startswith("reject_"):
        user_id = int(call.data.split("_")[1])
        bot.send_message(user_id, "❌ Оплата отклонена.")
        bot.answer_callback_query(call.id, "Пользователь уведомлен")
    
    # Убираем кнопки после нажатия
    try:
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=None
        )
    except:
        pass

if __name__ == "__main__":
    print("Тестовый бот запущен")
    bot.infinity_polling()

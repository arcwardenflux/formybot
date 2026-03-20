import telebot
from telebot import types
import time
import os

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 1203563417

PHOTO1 = "AgACAgIAAxkBAAPCaby-TyLffmfl3snkSpFvgXFowH0AAq8VaxsU9-hJ6PuyyuDXwlwBAAMCAAN5AAM6BA"
PHOTO2 = "AgACAgIAAxkBAANeabxJXgs7pRz5ol1lkJ6s8ITpIq0AAjEXaxu2pOFJGa0a13aqv0wBAAMCAAN5AAM6BA"

TEXT1 = 'Прежде чем совершить покупку прочитайте этот <a href="https://t.me/c/3850232762/3">пост</a>'
TEXT2 = '''Создание AI модели и заработок на ней💲
Цена: 50USDT
Остается у вас и дополняется всегда✅

Вы получите доступ к файлу 
— Manual AI MODELS📓, 
Доступ к гайду осуществляется по кнопке после оплаты. Так же когда оплата пройдёт успешно, Команда вручную проверяет вашу квитанцию через бота, и после её одобряет [в течении 12 часов] и кнопки.'''
TEXT3 = "TQj14bx3VVunwBfPTQNombG7FmyFbLedDS"
TEXT4 = "Отправьте боту скриншот оплаты. После проверки, вам будет открыт доступ."
TEXT5 = "✅ Оплата подтверждена! Вот ваш гайд:"
TEXT6 = "❌ Ваш скриншот не прошел проверку. Попробуйте еще раз или свяжитесь с поддержкой."
TEXT7 = "🔥 Скидка 50%% в течении 12 часов! 🔥\n\nУспей забрать гайд за полцены — 25 USDT вместо 50."

BUTTON1_TEXT = "Получить доступ"
BUTTON2_TEXT = "USDT TRC20"
BUTTON3_TEXT = "Отмена"
BUTTON4_TEXT = "Я оплатил✅"
BUTTON5_TEXT = "Оплатить со скидкой 50%%"

bot = telebot.TeleBot(TOKEN)
user_messages = {}
user_waiting_for_screenshot = set()

def delete_previous_messages(chat_id):
    if chat_id in user_messages:
        for msg_id in user_messages[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except:
                pass
        user_messages[chat_id] = []

def save_message_id(chat_id, message_id):
    if chat_id not in user_messages:
        user_messages[chat_id] = []
    user_messages[chat_id].append(message_id)

def send_guide(chat_id):
    try:
        with open('guide.pdf', 'rb') as file:
            bot.send_document(chat_id, file, caption=TEXT5)
            print(f"✅ Гайд отправлен пользователю {chat_id}")
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка отправки гайда: {e}")
        bot.send_message(chat_id, "❌ Ошибка при отправке гайда. Свяжитесь с поддержкой.")

@bot.message_handler(commands=['start'])
def start_cmd(message):
    chat_id = message.chat.id
    delete_previous_messages(chat_id)

    msg1 = bot.send_photo(chat_id, PHOTO1, caption=TEXT1, parse_mode='HTML')
    save_message_id(chat_id, msg1.message_id)

    time.sleep(0.5)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(BUTTON1_TEXT, callback_data="get_access"))
    msg2 = bot.send_message(chat_id, TEXT2, reply_markup=markup)
    save_message_id(chat_id, msg2.message_id)

    if chat_id != ADMIN_ID:
        bot.send_message(ADMIN_ID, f"🆕 Новый пользователь: {message.from_user.first_name} (@{message.from_user.username}) ID: {chat_id}")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "get_access":
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(BUTTON2_TEXT, callback_data="pay_usdt"),
            types.InlineKeyboardButton(BUTTON3_TEXT, callback_data="cancel")
        )
        msg3 = bot.send_message(chat_id, "Выберите способ оплаты:", reply_markup=markup)
        save_message_id(chat_id, msg3.message_id)
        bot.answer_callback_query(call.id)

    elif call.data == "pay_usdt":
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(BUTTON4_TEXT, callback_data="i_paid"),
            types.InlineKeyboardButton(BUTTON3_TEXT, callback_data="cancel")
        )
        msg4 = bot.send_photo(chat_id, PHOTO2, caption=TEXT3, reply_markup=markup)
        save_message_id(chat_id, msg4.message_id)
        bot.answer_callback_query(call.id)

    elif call.data == "i_paid":
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        msg5 = bot.send_message(chat_id, TEXT4)
        save_message_id(chat_id, msg5.message_id)
        user_waiting_for_screenshot.add(chat_id)
        bot.answer_callback_query(call.id, "Ожидаем скриншот...")

    elif call.data == "cancel":
        delete_previous_messages(chat_id)

        msg1 = bot.send_photo(chat_id, PHOTO1, caption=TEXT1, parse_mode='HTML')
        save_message_id(chat_id, msg1.message_id)
        time.sleep(0.5)

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTON1_TEXT, callback_data="get_access"))
        msg2 = bot.send_message(chat_id, TEXT2, reply_markup=markup)
        save_message_id(chat_id, msg2.message_id)
        bot.answer_callback_query(call.id, "Возврат в начало")

    elif call.data == "discount_pay":
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(BUTTON4_TEXT, callback_data="i_paid"),
            types.InlineKeyboardButton(BUTTON3_TEXT, callback_data="cancel")
        )
        msg4 = bot.send_photo(chat_id, PHOTO2, caption=TEXT3, reply_markup=markup)
        save_message_id(chat_id, msg4.message_id)
        bot.answer_callback_query(call.id)

    elif call.data.startswith("approve_"):
        user_id = int(call.data.split("_")[1])
        send_guide(user_id)
        try:
            bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=call.message.caption + "\n\n✅ Оплата подтверждена, гайд отправлен."
            )
        except:
            pass
        bot.answer_callback_query(call.id, "Гайд отправлен!")

    elif call.data.startswith("reject_"):
        user_id = int(call.data.split("_")[1])
        bot.send_message(user_id, TEXT6)
        try:
            bot.edit_message_caption(
                chat_id=chat_id,
                message_id=message_id,
                caption=call.message.caption + "\n\n❌ Оплата отклонена."
            )
        except:
            pass
        bot.answer_callback_query(call.id, "Пользователь уведомлен")

@bot.message_handler(content_types=['photo'])
def handle_screenshot(message):
    print(f"📸 Получено фото от {message.chat.id}")
    chat_id = message.chat.id

    if chat_id == ADMIN_ID:
        bot.reply_to(message, f"📸 File ID: `{message.photo[-1].file_id}`", parse_mode='Markdown')
        return

    if chat_id in user_waiting_for_screenshot:
        caption = f"🖼 Скриншот оплаты от {message.from_user.first_name} (@{message.from_user.username}) [ID:{chat_id}]"
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ Подтвердить оплату", callback_data=f"approve_{chat_id}"),
            types.InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{chat_id}")
        )
        
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, reply_markup=markup)
        bot.send_message(chat_id, "✅ Скриншот отправлен админу. Ожидайте проверки.")
        user_waiting_for_screenshot.remove(chat_id)
    else:
        bot.forward_message(ADMIN_ID, chat_id, message.message_id)

@bot.message_handler(func=lambda message: message.chat.id != ADMIN_ID and message.text)
def forward_text(message):
    sign = f"✉️ От {message.from_user.first_name} (@{message.from_user.username}) [ID:{message.chat.id}]"
    bot.send_message(ADMIN_ID, f"{sign}\n\n{message.text}")

@bot.message_handler(commands=['send'], func=lambda message: message.chat.id == ADMIN_ID)
def send_to_user(message):
    try:
        parts = message.text.split(maxsplit=2)
        if len(parts) < 3:
            bot.reply_to(message, "❌ Использование: /send user_id текст")
            return
        user_id = parts[1]
        text = parts[2]
        try:
            user_id = int(user_id)
        except:
            bot.reply_to(message, "❌ ID должен быть числом")
            return
        bot.send_message(user_id, text)
        bot.reply_to(message, f"✅ Отправлено пользователю {user_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

@bot.message_handler(commands=['discount'], func=lambda message: message.chat.id == ADMIN_ID)
def send_discount_to_user(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Использование: /discount user_id")
            return
        user_id = int(parts[1])

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(BUTTON5_TEXT, callback_data="discount_pay"))

        bot.send_message(
            user_id,
            "🔥 Скидка 50%% в течении 12 часов! 🔥\n\nУспей забрать гайд за полцены — 25 USDT вместо 50.",
            reply_markup=markup
        )
        bot.reply_to(message, f"✅ Скидка отправлена пользователю {user_id}")
    except Exception as e:
        bot.reply_to(message, f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("🤖 Бот с автовыдачей запущен")
    bot.infinity_polling()

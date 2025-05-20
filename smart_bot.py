import openai
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# === OpenAI API Key ===
openai.api_key = "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"

# === Telegram Bot Functions ===

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Bot Info", callback_data='info')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Welcome! Amar sathe kotha bolte paro ba button use koro:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    data = query.data

    if data == 'info':
        query.edit_message_text("Ami ekta smart Telegram bot. Tumi amar sathe kotha bolte paro.")
    elif data == 'help':
        query.edit_message_text("Just amar sathe kotha bolo, ami reply debo!")

def chat_with_gpt(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # free version
        messages=[{"role": "user", "content": text}]
    )
    return response['choices'][0]['message']['content']

def handle_message(update: Update, context: CallbackContext):
    user_text = update.message.text
    try:
        reply = chat_with_gpt(user_text)
    except Exception as e:
        reply = "Sorry! GPT theke reply pawa jacche na."
    update.message.reply_text(reply)

def main():
    updater = Updater("7745028616:AAHY2xe1EsnSu_GpRb_z3N7vGrSCEO4hM2Y", use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

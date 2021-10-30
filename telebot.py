import logging
import markovify
import os
import prediction
import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, ConversationHandler, Filters)

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
text_path = "./data/female"
KOMPLEMENT = 'комплемент'
PREDICT = 'гра'


def start(update, context):
    chat_id = update.message.chat_id
    custom_keyboard = [[KOMPLEMENT, "gra"], ["game", PREDICT]]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=chat_id,
                              text="Це супер бот. Визначає в яку гру ти граеш по картинці",
                              reply_markup=reply_markup)


def error(update, context):
    logger.warning('update "%s" casused error "%s"', update, context.error)


def cancel(update, context):
    return ConversationHandler.END


def get_model(filename):
    with open(filename, encoding="utf-8") as f:
        text = f.read()

    return markovify.Text(text)


def photo(update, context):
    # context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.UPLOAD_PHOTO)

    userId = update.message.chat_id
    print(userId)
    # download image from bot
    file_id = update.message.photo[-1]
    new_image = context.bot.get_file(file_id)
    new_image.download('files/to_watermark_pic.png')
    # upload image to bot
    # context.bot.send_photo(chat_id=userId, photo=open('files/01.png', 'rb'))
    result_prediction = prediction.predict_game("files/to_watermark_pic.png")

    update.message.reply_text(result_prediction)


def text_handler(update, context):
    print("text message")
    final_message = ''
    get_message_bot = update.message.text.strip().lower()
    if get_message_bot == KOMPLEMENT:
        sometext = get_model(text_path)
        final_message = sometext.make_sentence()

    if final_message == '':
        final_message = "<b>Param pram pam</b>"

    context.bot.send_message(update.message.chat_id, final_message, parse_mode='html')

def main():
    logger.info("Loading handlers for telegram bot")
    updater = Updater(API_TOKEN, use_context=True)
    dp = updater.dispatcher

    photo_handler = MessageHandler(Filters.photo, photo)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("cancel", cancel))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    dp.add_handler(photo_handler)
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

from bot_sivim._secrets import get_secret
from bot_sivim._fiber import get_fiber_data
import logging

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CITY, STREET, HOUSE_NUM = range(3)


def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Enter City')
    return CITY


def city(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    city = update.message.text

    logger.info(f'City of {user.first_name}: {city}')

    context.user_data['city'] = city

    update.message.reply_text('Enter Street')

    return STREET


def street(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    street = update.message.text

    logger.info(f'Street of {user.first_name}: {street}')

    context.user_data['street'] = street

    update.message.reply_text('Enter House Number')

    return HOUSE_NUM

def house_num(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    house_num = update.message.text
    city = context.user_data['city']
    street = context.user_data['street']

    logger.info(f'Address of {user.first_name}: {city}, {street}, {house_num}')
    update.message.reply_text('Fetching fiber data...')
    data = get_fiber_data(city, street, house_num)
    text = '\n'.join(f'{company}: {available}' for company, available in data)
    text = f'{city}, {street}, {house_num}\n\n{text}\n'
    update.message.reply_text(text)

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    updater = Updater(get_secret('telegram'))

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CITY: [MessageHandler(Filters.text & ~Filters.command, city)],
            STREET: [MessageHandler(Filters.text & ~Filters.command, street)],
            HOUSE_NUM: [MessageHandler(Filters.text & ~Filters.command, house_num)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

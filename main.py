import os.path
import logging
import datetime
import re

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from state import State
from authorized_chat_ids_filter import AuthorizedChatIdsFilter
import credentials_json
import my_utils


states_control = {
    0: State('None',
             'Please enter name of the donor.',
             State.validate_nothing),
    1: State('donor',
             'Please enter the date of donation, e.g. January 2021.',
             State.validate_nothing),
    2: State('date',
             'Please enter the received amount in Euros.',
             State.validate_nothing),
    3: State('donation_euros',
             'Please enter the exchange rate for Euros to Tomans.',
             State.validate_nothing),
    4: State('exchange_rate',
             'Please enter the transferred amount to charity in Tomans.',
             State.validate_nothing),
    5: State('donation_tomans',
             'Please send the receipt of the transferred amount to charity.',
             State.validate_nothing)
}


def start(update, context):
    context.user_data.clear()
    state = 0
    update.message.reply_text(states_control[state].next_input_request)
    context.user_data['state'] = state + 1


def end(update, context):
    context.user_data.clear()


def process_text(update, context):
    received_message = update.message.text
    state = context.user_data.get('state', 'None')

    if state == 'None':
        print_help(update)

    elif state > 0 and state < 6:
        if states_control[state].validate_input(received_message):
            context.user_data[states_control[state].name] = received_message
            update.message.reply_text(states_control[state].next_input_request)
            context.user_data['state'] = state + 1

    elif state == 6:
        print(context.user_data)


def process_photo(update, context):
    state = context.user_data.get('state', 'None')
    if state == 6:
        receipt = context.bot.getFile(update.message.photo[-1].file_id)
        receipt_path = my_utils.get_tmp_file_dir('jpg')
        receipt.download(receipt_path)
        donor = context.user_data['donor']
        date = context.user_data['date']
        donation_euros = context.user_data['donation_euros']
        exchange_rate = context.user_data['exchange_rate']
        donation_tomans = context.user_data['donation_tomans']
        pdf = my_utils.create_pdf(donor, date, donation_euros, exchange_rate, donation_tomans, receipt_path)
        context.bot.send_document(chat_id=update.effective_chat.id, document=open(pdf, 'rb'))


def print_help(update):
    message = 'Please start the bot with one of the following commands:\n\n'
    message += '/start - start a session\n'
    message += '/end - end the session'
    update.message.reply_text(message)

# Validating credentials.json
if not credentials_json.is_valid():
    raise SyntaxError('Non-existing or invalid credentials.json file.')

# Configure the logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Create the updater
updater = Updater(token=credentials_json.get_bot_token(), use_context=True)
dispatcher = updater.dispatcher

# Setup command handler for 'start'
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Setup command handler for 'end'
end_handler = CommandHandler('end', end)
dispatcher.add_handler(end_handler)

# Setup text message handler
authorized_chat_ids = credentials_json.get_authorized_chat_ids()
authorized_chat_ids_filter = AuthorizedChatIdsFilter(authorized_chat_ids)
text_handler = MessageHandler(Filters.text & (~Filters.command) & authorized_chat_ids_filter, process_text)
dispatcher.add_handler(text_handler)

# Setup photo message handler
photo_handler = MessageHandler(Filters.photo, process_photo)
dispatcher.add_handler(photo_handler)

updater.start_polling()
updater.idle()

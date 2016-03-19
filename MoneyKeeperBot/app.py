# coding: utf-8
import logging
from telebot import types
from MoneyKeeperBot.misc import get_info, login_required
from MoneyKeeperBot import redis_helpers
from MoneyKeeperBot.next_message_callbacks import category_chosen, account_to_chosen
from MoneyKeeperBot.settings import MONEYKEEPER_URL, DEFAULT_KEYBOARD, BOT

logger = logging.getLogger(__name__)


@BOT.message_handler(commands=['help'])
def send_help(message):
    CMD = ['income', 'expense', 'transfer']
    user_id = message.from_user.id
    BOT.send_message(user_id, '\n'.join(['/{0} - post {0} transaction'.format(kind) for kind in CMD]))


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    try:
        if 'authenticated' in message.text:
            redis_helpers.store_api_user(user_id)
            redis_helpers.store_resource('account', user_id)
            redis_helpers.store_resource('category', user_id)
            BOT.send_message(user_id, 'Authentication successful!', reply_markup=DEFAULT_KEYBOARD)
        else:
            welcome_msg = ('''
Hi, %(username)s!\n\nI\'m simple helper bot for [MoneyKeeper](%(url)s).
My responsibilities is: send your transactions to [MoneyKeeper](%(url)s) and show info from your accounts.
To proceed you will need authenticate [here](%(auth_url)s)
In case of mistrust you can visit the source code on my creators [GitHub](https://github.com/ilov3).
            ''')
            kwargs = {
                'username': message.from_user.username,
                'url': MONEYKEEPER_URL,
                'auth_url': MONEYKEEPER_URL + 'auth/%s' % user_id
            }
            BOT.send_message(user_id, welcome_msg % kwargs, reply_markup=DEFAULT_KEYBOARD, parse_mode='Markdown', disable_web_page_preview=True)
    except Exception as e:
        logger.error(e)


@BOT.message_handler(commands=['income'])
@login_required
def income(message):
    BOT.register_next_step_handler(message, category_chosen)
    user_id = message.from_user.id
    redis_helpers.store_transaction_kind('income', user_id)
    token = redis_helpers.get_api_token(user_id)
    try:
        if token:
            redis_helpers.update_stored_resource('category', user_id)
            categories = redis_helpers.get_stored_resource('category', user_id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(*[cat['name'] for cat in categories if cat['kind'] == 'inc'])
            markup.add('/cancel')
            BOT.send_message(user_id, 'Choose category:', reply_markup=markup)
        else:
            BOT.send_message(user_id, 'Authenticate first!')
    except Exception as e:
        logger.warn(e)


@BOT.message_handler(commands=['expense'])
@login_required
def expense(message):
    BOT.register_next_step_handler(message, category_chosen)
    user_id = message.from_user.id
    redis_helpers.store_transaction_kind('expense', user_id)
    token = redis_helpers.get_api_token(user_id)
    try:
        if token:
            redis_helpers.update_stored_resource('category', user_id)
            categories = redis_helpers.get_stored_resource('category', user_id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(*[cat['name'] for cat in categories if cat['kind'] == 'exp'])
            markup.add('/cancel')
            BOT.send_message(user_id, 'Choose category:', reply_markup=markup)
        else:
            BOT.send_message(user_id, 'Authenticate first!')
    except Exception as e:
        logger.warn(e)


@BOT.message_handler(commands=['transfer'])
@login_required
def transfer(message):
    BOT.register_next_step_handler(message, account_to_chosen)
    user_id = message.from_user.id
    redis_helpers.store_transaction_kind('transfer', user_id)
    token = redis_helpers.get_api_token(user_id)
    try:
        if token:
            redis_helpers.update_stored_resource('account', user_id)
            accounts = redis_helpers.get_stored_resource('account', user_id)
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            markup.add(*[acc['name'] for acc in accounts])
            markup.add('/cancel')
            BOT.send_message(user_id, 'Choose account transfer to:', reply_markup=markup)
        else:
            BOT.send_message(user_id, 'Authenticate first!')
    except Exception as e:
        logger.warn(e)


@BOT.message_handler(commands=['info'])
@login_required
def info(message):
    user_id = message.from_user.id
    redis_helpers.update_stored_resource('account', user_id)
    get_info(user_id)


@BOT.message_handler(commands=['cancel'])
def cancel(message):
    user_id = message.from_user.id
    redis_helpers.flush_transaction_fields(user_id)
    BOT.send_message(user_id, 'Transaction cancelled!', reply_markup=DEFAULT_KEYBOARD)


BOT.polling(none_stop=True, interval=0, timeout=3)

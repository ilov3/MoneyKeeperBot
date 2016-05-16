# coding=utf-8
import logging
from telebot import types
import redis_helpers
from MoneyKeeperBot.settings import BOT
from MoneyKeeperBot.misc import send_transaction, get_info, cancellable

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


@cancellable
def category_chosen(message):
    BOT.register_next_step_handler(message, account_chosen)
    category = message.text
    user_id = message.from_user.id
    redis_helpers.store_transaction_to(category, user_id)
    accounts = redis_helpers.get_stored_resource('account', user_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(*[acc['name'].encode('utf-8') for acc in accounts])
    markup.add('/cancel')
    BOT.send_message(user_id, 'Choose account:', reply_markup=markup)


@cancellable
def account_to_chosen(message):
    BOT.register_next_step_handler(message, account_chosen)
    account_to = message.text
    user_id = message.from_user.id
    redis_helpers.store_transaction_to(account_to, user_id)
    accounts = redis_helpers.get_stored_resource('account', user_id)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(*[acc['name'].encode('utf-8') for acc in accounts])
    markup.add('/cancel')
    BOT.send_message(user_id, 'Choose account:', reply_markup=markup)


@cancellable
def account_chosen(message):
    BOT.register_next_step_handler(message, amount_given)
    account = message.text
    user_id = message.from_user.id
    redis_helpers.store_transaction_from(account, user_id)
    BOT.send_message(user_id, 'Give amount:', reply_markup=types.ReplyKeyboardHide())


@cancellable
def amount_given(message):
    user_id = message.from_user.id
    try:
        amount = message.text
        redis_helpers.store_transaction_amount(amount, user_id)
        code = send_transaction(user_id)
        logger.info(code)
        if code == 201:
            get_info(user_id)
        else:
            BOT.send_message(user_id, 'Something went wrong...')
    except Exception as e:
        logger.error(e)

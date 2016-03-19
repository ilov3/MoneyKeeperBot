# coding=utf-8
import logging
import requests
import arrow
from MoneyKeeperBot.redis_helpers import get_api_token, get_stored_resource, update_stored_resource
from MoneyKeeperBot.settings import API_URL, REDIS, BOT, DEFAULT_KEYBOARD

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


def send_transaction(user_id):
    url = API_URL + 'transaction/'
    kind = REDIS.hget('%s:transaction' % user_id, 'kind')
    category_or_transfer_to = 'category' if kind != 'trn' else 'transfer_to_account'
    payload = {
        'account': REDIS.hget('%s:transaction' % user_id, 'from'),
        category_or_transfer_to: REDIS.hget('%s:transaction' % user_id, 'to'),
        'amount': REDIS.hget('%s:transaction' % user_id, 'amount'),
        'kind': kind,
        'user': REDIS.hget(user_id, 'api_user'),
        'date': arrow.now().format('YYYY-MM-DD'),
    }
    req = requests.post(url, data=payload, headers={'authorization': 'JWT ' + get_api_token(user_id)})
    update_stored_resource('account', user_id)
    return req.status_code


def get_info(user_id):
    accounts = get_stored_resource('account', user_id)
    balances = '\n'.join(['%s: %s' % (acc['name'], acc['get_balance']) for acc in accounts])
    balances += '\nTotal: %s' % sum([acc['get_balance'] for acc in accounts])
    BOT.send_message(user_id, balances, reply_markup=DEFAULT_KEYBOARD)


def cancellable(func):
    def wrapper(message):
        if message.text == '/cancel':
            return
        func(message)

    return wrapper

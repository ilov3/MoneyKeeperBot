# coding=utf-8
import json
import logging
import requests
from settings import API_URL, REDIS

__author__ = 'ilov3'
logger = logging.getLogger(__name__)


def get_api_token(user_id):
    return REDIS.hget(user_id, 'token')


def store_api_user(user_id):
    url = API_URL + 'conf/'
    api_user = requests.get(url, headers={'authorization': 'JWT ' + get_api_token(user_id)}).json().get('username')
    REDIS.hset(user_id, 'api_user', api_user)


def store_resource(resource, user_id):
    url = API_URL + resource
    resources = requests.get(url, headers={'authorization': 'JWT ' + get_api_token(user_id)}).text.encode('utf-8')
    REDIS.hset(user_id, resource, resources)


def get_stored_resource(resource, user_id):
    return json.loads(REDIS.hget(user_id, resource))


def update_stored_resource(resource, user_id):
    store_resource(resource, user_id)


def store_transaction_kind(kind, user_id):
    kinds_map = {'income': 'inc', 'expense': 'exp', 'transfer': 'trn'}
    REDIS.hset('%s:transaction' % user_id, 'kind', kinds_map[kind])


def store_transaction_from(fr, user_id):
    REDIS.hset('%s:transaction' % user_id, 'from', fr)


def store_transaction_to(to, user_id):
    REDIS.hset('%s:transaction' % user_id, 'to', to)


def store_transaction_amount(amount, user_id):
    REDIS.hset('%s:transaction' % user_id, 'amount', amount)


def flush_transaction_fields(user_id):
    REDIS.delete('%s:transaction' % user_id)

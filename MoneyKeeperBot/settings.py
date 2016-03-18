# coding=utf-8
import logging
import os
import redis
import telebot
from telebot import types
from utils import setup_env

setup_env()

__author__ = 'ilov3'
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

MONEYKEEPER_URL = os.environ.get('MONEYKEEPER_URL')

API_URL = MONEYKEEPER_URL + 'api/'

REDIS = redis.StrictRedis(host='localhost', port=6379, db=0)

DEFAULT_KEYBOARD = types.ReplyKeyboardMarkup(resize_keyboard=True)
DEFAULT_KEYBOARD.add('/info', '/income', '/expense', '/transfer')
BOT = telebot.TeleBot(TELEGRAM_TOKEN)

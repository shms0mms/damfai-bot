

import statistics
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from const import markups, analytics_markups
# markups
profile = KeyboardButton(text=markups['profile'])
logout = KeyboardButton(text=markups['logout']) 
login = KeyboardButton(text=markups['login'])
speech_book = KeyboardButton(text=markups['speech/book'])
statistics = KeyboardButton(text=markups['statistics'])
analytics = KeyboardButton(text=markups['analytics'])
# Создаем клавиатуру для неавторизованного пользователя
user_markup = ReplyKeyboardMarkup(keyboard=[[login], [speech_book]], resize_keyboard=True)

# Создаем клавиатуру для авторизованного пользователя


auth_user_markup = ReplyKeyboardMarkup(keyboard=[[speech_book, profile], [statistics, analytics], [logout]], resize_keyboard=True)


analytics_markup = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=i[1], callback_data=i[0])] for i in analytics_markups.items()])

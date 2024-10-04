

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from const import markups

profile = KeyboardButton(text=markups['profile'])
settings = KeyboardButton(text=markups['settings'])
logout = KeyboardButton(text=markups['logout']) 
feedback = KeyboardButton(text=markups['feedback'])
login = KeyboardButton(text=markups['login'])
user_markup = ReplyKeyboardMarkup(keyboard=[[profile, settings, feedback, login]], resize_keyboard=True)
auth_user_markup = ReplyKeyboardMarkup(keyboard=[[profile, settings, logout, feedback]], resize_keyboard=True)


from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from const import markups
# markups
profile = KeyboardButton(text=markups['profile'])
logout = KeyboardButton(text=markups['logout']) 
feedback = KeyboardButton(text=markups['feedback'])
login = KeyboardButton(text=markups['login'])
speech_book = KeyboardButton(text=markups['speech/book'])
user_markup = ReplyKeyboardMarkup(keyboard=[[feedback, login, speech_book]], resize_keyboard=True)
auth_user_markup = ReplyKeyboardMarkup(keyboard=[[profile, logout, feedback, speech_book]], resize_keyboard=True)
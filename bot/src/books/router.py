import logging
import os
import requests
from sqlalchemy import select
from aiogram import Router, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from bot.src.utils.get_markup import get_markup
from utils.extract_book_index import extract_book_index
from server.src.books.books_models import Book
from config import config
from markups import markups, user_markup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
class ChooseBookState(StatesGroup):
    choose = State()

router = Router(name="books")

@router.message(F.text == markups['speech/book'])
async def choose_book_handler(msg: Message, session: AsyncSession, state: FSMContext): 
    books = await session.scalars(select(Book))
    books = books.all()
	
    keyboard = []
    if len(books):
        for book in books:
            keyboard.append(KeyboardButton(text=f"{book.id}. {book.title}"))
    
    markup = ReplyKeyboardMarkup(keyboard=[keyboard], resize_keyboard=True)
    if len(keyboard):
        await state.set_state(ChooseBookState.choose)
        await msg.answer(text="Выберите книгу из предложенного списка", reply_markup=markup)
    else: 
        await msg.answer(text='Книг пока нет.')

@router.message(ChooseBookState.choose)
async def speech_and_return_to_user(msg: Message, session: AsyncSession, state: FSMContext):
    # if msg.text not in [button.text for button in keyboard]:
        # return await msg.answer('Книга не найдена в списке.')
    
    book_id = extract_book_index(msg.text)
    book = await session.scalar(select(Book).where(Book.id == book_id))
    me = msg.from_user.first_name
    await state.clear()
    if book:
        try:
            url = config.env.SPEECH_URL
            token = config.env.SPEECH_ACCESS_TOKEN
            headers = {"Authorization": f"Bearer {token}", 'Content-Type': 'application/ssml'}
            data = f"Привет, {me}!"

            response = requests.post(url, headers=headers, data=data, verify=False)
            if response.status_code == 200:
                wav_data = response.content

                file_path = f"audios/books/book_{book.id}.wav"
                os.makedirs(os.path.dirname(file_path), exist_ok=True) 
                with open(file_path, "wb") as f:
                    f.write(wav_data)
                markup = await get_markup(msg.from_user.id, session)
				
                await msg.answer_document(document=FSInputFile(path=file_path, filename=f"{msg.text}.wav"), reply_markup=markup)
                
            else:
                logging.error(f"Request from SpeechAPI failed with status code {response.status_code}")
                return await msg.answer('Что-то пошло не так, попробуйте еще раз.')

        except requests.exceptions.SSLError as ssl_error:
            logging.error(f"SSL Error occurred: {ssl_error}")
        except requests.exceptions.RequestException as req_error:
            logging.error(f"Request Error: {req_error}")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
    else:
        return await msg.answer('Такая книга не найдена в базе данных!')
    

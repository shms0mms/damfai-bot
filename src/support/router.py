
from .models import Message
from aiogram import F, Router, types
from sqlalchemy.ext.asyncio import AsyncSession
from const import markups
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
router = Router(name="support")

class FeedbackState(StatesGroup):
    wait = State()


async def save_message(message: types.Message, session: AsyncSession) -> None:
    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text
    message = Message(user_id=user_id, username=username, text=text)
    session.add(message)
    await session.commit()




@router.message(F.text == markups['feedback'])
async def feedback_handler(msg: types.Message, session: AsyncSession, state: FSMContext):
    await state.set_state(FeedbackState.wait)
    await msg.answer('Приветствуем! Напиши свой отзыв о нашей платформе damfai, и напиши нам, если нашел какой-либо баг 🙏')
    
@router.message(FeedbackState.wait)    
async def feedback_messages(msg: types.Message, session: AsyncSession, state: FSMContext):
        await save_message(msg, session)
        await msg.answer('Ваше сообщение успешно отправлено администрации на проверку и будет рассмотрено в ближайшее время.')
        await state.clear()
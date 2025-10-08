from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import *
from filters.chat_types import ChatTypeFilter
from handlers.user.new_user import handle_new_user
from kbds.kbs import *
from utils.texts import *

start_router = Router()
start_router.message.filter(ChatTypeFilter(["private"]))
start_router.callback_query.filter(ChatTypeFilter(["private"]))

@start_router.message(CommandStart())
async def handle_start_command(message: types.Message, session: AsyncSession, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = message.from_user.username

    try:
        user = await orm_get_user(session, user_id)

    except Exception as e:
        user = None

    if not user:
        await handle_new_user(message, session, state, user_id, first_name, referer_id)
        return

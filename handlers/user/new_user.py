from typing import Union

from aiogram import types
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from database.orm_query import orm_add_user, orm_verify_referral, orm_get_referer, add_money
from kbds.kbs import get_channels_btns
from utils.texts import get_not_ref_reg_text, get_ref_reg_text


# TODO использовать logger вместо print 
async def handle_new_user(
        event: Union[types.Message, types.CallbackQuery],
        session: AsyncSession,
        state: FSMContext,
        user_id: int,
        first_name: str,
        referer_id: str = None) -> bool:
    if isinstance(event, types.Message):
        message = event
    elif isinstance(event, types.CallbackQuery):
        message = event.message
    else:
        print(f"Не является Message или CallbackQuery handle_new_user")
        return

    try:
        await orm_add_user(session, user_id, message.from_user.username, referer_id, first_name)

        return True

    except Exception as ex:
        print(f"Не удалось зарегстироровать нового пользователя с ником {message.from_user.username} c id {message.from_user.user_id}")

    return False



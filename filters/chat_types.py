from abc import ABC
from typing import Union

from aiogram.filters import Filter
from aiogram import Bot, types
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_get_channels, orm_check_user_request, orm_get_admins


class ChatTypeFilter(Filter):
    def __init__(self, chat_types: list[str]) -> None:
        self.chat_types = chat_types

    async def __call__(self, event: Union[types.Message, types.CallbackQuery]) -> bool:
        if isinstance(event, types.Message):
            message = event
        elif isinstance(event, types.CallbackQuery):
            message = event.message
        return message.chat.type in self.chat_types


class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, event: Union[types.Message, types.CallbackQuery], bot: Bot, session: AsyncSession) -> bool:
        admins_list = []
        try:
            admins_list = await orm_get_admins(session)
            print(f"ID админов: {admins_list}")
        except Exception as e:
            print(f"Ошибка при получении админов: {e}")

        return event.from_user.id in admins_list


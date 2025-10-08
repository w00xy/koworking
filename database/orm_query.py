from aiogram.loggers import event
from sqlalchemy import select, update, delete, values, desc
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError, MultipleResultsFound, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.util.langhelpers import repr_tuple_names

from config import MONEY_AMOUNT
from database.engine import session_maker
from database.models import User, Referral, Channel, ChannelRequests, UserHistory, HelpMessage


async def orm_get_user(session: AsyncSession, user_id: int) -> User:
    query = select(User).where(User.user_id == user_id)

    user = await session.execute(query)

    # Use fetchone() to get the first result
    user = user.scalar_one_or_none()

    return user



async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    username: str,
    referer_id: int,
    user_first_name: str,
    referrals_total: int = None,
):
    """Adds a new user to the database, separating data into User and Referral tables.

    Args:
        session: A SQLAlchemy asynchronous session object.
        user_id: The unique identifier for the new user.
        referer_id: The ID of the user who referred this new user.
        user_first_name: The first name of the new user.
        referrals_total: The total number of referrals for this user.
    """

    new_user = User(
        user_id=user_id,
        user_first_name=user_first_name,
        username=username,
    )
    session.add(new_user)

    new_referral = Referral(
        user_id=user_id,
        referer_id=referer_id,
        is_verified=False,
    )
    session.add(new_referral)

    await session.commit()


from sqlalchemy import String, BigInteger, Float, Integer, ForeignKey, DateTime, func, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    user_first_name: Mapped[str] = mapped_column((String(40)), nullable=True)
    username: Mapped[str] = mapped_column((String(60)), nullable=True)
    balance: Mapped[float] = mapped_column(Float, default=0)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_creator: Mapped[bool] = mapped_column(Boolean, default=False)

from typing import List

from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email = mapped_column(Text)
    password = mapped_column(Text)
    auth_token = mapped_column(Text)
    reset_token = mapped_column(Text)
    reset_timestamp = mapped_column(Text)


class Content(Base):
    __tablename__ = "content"

    id: Mapped[int] = mapped_column(primary_key=True)
    shape_identifier = mapped_column(Text)
    fields: Mapped[List["ContentField"]] = relationship()


class ContentField(Base):
    __tablename__ = "content_fields"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier = mapped_column(Text)
    value = mapped_column(Text)
    content_id: Mapped[int] = mapped_column(ForeignKey("content.id"))

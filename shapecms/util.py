from flask.sessions import SessionMixin
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from shapecms.db import User


def is_authenticated(db: Engine, session: SessionMixin) -> bool:
    if "auth_token" in session:
        token: str = session.get("auth_token")
        stmt = select(User).where(User.auth_token == token)

        with Session(db) as s:
            return s.execute(stmt).first() is not None

    return False


def is_setup(db: Engine) -> bool:
    stmt = select(User)

    with Session(db) as s:
        return s.execute(stmt).first() is not None


from typing import List

from flask import request, session
from flask.views import MethodView
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from shapecms import Shape
from shapecms.db import User


class PageView(MethodView):
    db: Engine = None

    def __init__(self, **kwargs):
        if "db" in kwargs:
            self.db = kwargs.get("db")


class AdminPageView(MethodView):
    shapes: List[Shape] = []
    db: Engine = None

    def __init__(self, **kwargs):
        if "db" in kwargs:
            self.db = kwargs.get("db")

        if "shapes" in kwargs:
            for shape_callable in kwargs.get("shapes"):
                shape_instance = shape_callable(request)
                self.shapes.append(shape_instance)

    def is_authenticated(self) -> bool:
        if "auth_token" in session:
            token: str = session.get("auth_token")
            stmt = select(User).where(User.auth_token == token)

            with Session(self.db) as s:
                return s.execute(stmt).first() is not None

        return False

    def is_setup(self) -> bool:
        stmt = select(User)

        with Session(self.db) as s:
            return s.execute(stmt).first() is not None

    def compute_injected_css(self) -> List[str]:
        css = []

        for shape in self.shapes:
            for field in shape.fields:
                for css_item in field.injected_css:
                    if css.count(css_item) == 0:
                        css.append(css_item)

        return css

    def compute_injected_js(self) -> List[str]:
        css = []

        for shape in self.shapes:
            for field in shape.fields:
                for css_item in field.injected_css:
                    if css.count(css_item) == 0:
                        css.append(css_item)

        return css

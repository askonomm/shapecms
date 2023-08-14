from typing import List
from flask.views import MethodView
from sqlalchemy import Engine
from shapecms import Shape


class AdminPageView(MethodView):
    shapes: List[Shape] = []
    db: Engine = None

    def __init__(self, **kwargs):
        if "db" in kwargs:
            self.db = kwargs.get("db")

        if "shapes" in kwargs:
            self.shapes = kwargs.get("shapes")

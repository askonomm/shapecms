from typing import List

from flask import request
from flask.views import MethodView
from sqlalchemy import Engine

from shapecms import Shape


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

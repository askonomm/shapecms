from typing import List, Type
from flask import Flask, Blueprint
from sqlalchemy import create_engine, Engine

from shapecms.db import Base
from shapecms.shape import Shape
from shapecms.page_views import PageView, AdminPageView
from shapecms.views.main import MainView
from shapecms.views.login import LoginView
from shapecms.views.setup import SetupView


class ShapeCMS:
    """An instance of ShapeCMS"""
    shapes: List[Shape] = []
    app: Flask = None
    client: Blueprint = None
    db: Engine = None

    def __init__(self, **kwargs):
        self.app = Flask(__name__, template_folder="./templates")

        # set client
        if "import_name" in kwargs:
            self.client = Blueprint("client", kwargs.get("import_name"), template_folder="./templates")

        # init db
        if "connection_uri" in kwargs:
            self.db = create_engine(kwargs.get("connection_uri"), echo=True)
            self.init_db()

        # create shapes
        if "shapes" in kwargs:
            self.shapes = kwargs.get("shapes")

        # add built-in routes
        self._add_view("/admin", MainView)
        self._add_view("/admin/setup", SetupView)
        self._add_view("/admin/login", LoginView)

    def _add_view(self, path: str, view_class: Type[AdminPageView]):
        view_name = view_class.__name__
        view_func = view_class.as_view(view_name, db=self.db, shapes=self.shapes)
        self.app.add_url_rule(path, view_func=view_func)

    def add_view(self, path: str, view_class: Type[PageView]):
        view_name = view_class.__name__
        self.client.add_url_rule(path, view_func=view_class.as_view(view_name, db=self.db))

    def init_db(self):
        Base.metadata.create_all(self.db)

    def start(self):
        self.app.register_blueprint(self.client)

        return self.app

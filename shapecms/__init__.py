from typing import List, Type
from flask import Flask, Blueprint
from sqlalchemy import create_engine, Engine

from shapecms.db import Base
from shapecms.shape import Shape
from shapecms.page_views import PageView, AdminPageView
from shapecms.views.admin import AdminView
from shapecms.views.admin_login import AdminLoginView
from shapecms.views.admin_setup import AdminSetupView


class ShapeCMS:
    """An instance of ShapeCMS"""
    shapes: List[Shape] = []
    app = None
    client = None
    db: Engine = None

    def __init__(self, **kwargs):
        self.app = Flask(__name__, template_folder="./templates")

        # set client
        if "import_name" in kwargs:
            self.client = Blueprint("client", kwargs.get("import_name"), template_folder="./templates")

        # init db
        if "connection_uri" in db:
            self.db = create_engine(kwargs.get("connection_uri"), echo=True)
            self.init_db()

        # create shapes
        if "shapes" in db:
            self.shapes = kwargs.get("shapes")

        # add built-in routes
        self._add_core_url("/admin", AdminView, "admin")
        self._add_core_url("/admin/setup", AdminSetupView, "admin_setup")
        self._add_core_url("/admin/login", AdminLoginView, "admin_login")

    def _add_core_url(self, rule: str, view_class: Type[AdminPageView], view_name: str):
        view_func = view_class.as_view(view_name, db=self.db, shapes=self.shapes)
        self.app.add_url_rule(rule, view_func=view_func)

    def add_url(self, rule: str, view_class: Type[PageView], view_name: str):
        self.client.add_url_rule(rule, view_func=view_class.as_view(view_name, db=self.db))

    def init_db(self):
        Base.metadata.create_all(self.db)

    def start(self):
        self.app.register_blueprint(self.client)

        return self.app

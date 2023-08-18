from typing import List, Type
from flask import Flask, Blueprint
from sqlalchemy import create_engine, Engine

from shapecms.db import Base
from shapecms.shape import Shape
from shapecms.page_views import PageView, AdminPageView
from shapecms.views.api.update_field import APIUpdateFieldView
from shapecms.views.content import ContentView
from shapecms.views.content_add import ContentAddView
from shapecms.views.content_edit import ContentEditView
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
            self.client = Blueprint("client", kwargs.get(
                "import_name"), template_folder="./templates")

        # init db
        if "connection_uri" in kwargs:
            self.db = create_engine(kwargs.get("connection_uri"), echo=True)
            self.__init_db()

        # create shapes
        if "shapes" in kwargs:
            self.shapes = kwargs.get("shapes")

        # create views
        if "views" in kwargs:
            for path, view in kwargs.get("views").items():
                self.__add_view(path, view)

        # add built-in routes
        self.__add_admin_view("/admin", MainView)
        self.__add_admin_view("/admin/setup", SetupView)
        self.__add_admin_view("/admin/login", LoginView)
        self.__add_admin_view("/admin/content/<identifier>", ContentView)
        self.__add_admin_view(
            "/admin/content/<identifier>/add", ContentAddView)
        self.__add_admin_view(
            "/admin/content/<identifier>/edit/<id>", ContentEditView)
        self.__add_admin_view(
            "/admin/api/content/<content_id>/field/<f_id>", APIUpdateFieldView)

    def __add_admin_view(self, path: str, view_class: Type[AdminPageView]):
        view_name = view_class.__name__
        view_func = view_class.as_view(
            view_name, db=self.db, shapes=self.shapes)
        self.app.add_url_rule(path, view_func=view_func)

    def __add_view(self, path: str, view_class: Type[PageView]):
        view_name = view_class.__name__
        self.client.add_url_rule(
            path, view_func=view_class.as_view(view_name, db=self.db))

    def __init_db(self):
        Base.metadata.create_all(self.db)

    def start(self):
        self.app.register_blueprint(self.client)

        return self.app

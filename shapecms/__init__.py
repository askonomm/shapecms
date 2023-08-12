from typing import List
from flask import Flask
from shapecms.shape import Shape
from shapecms.shape_view import PageView
from shapecms.views.admin import AdminView


class ShapeCMS:
    """An instance of ShapeCMS"""
    shapes: List[Shape] = []
    app = None

    def __init__(self):
        self.app = Flask(__name__)

        # add built-in routes
        self.add_url("/admin", AdminView(), "admin")

    def add_shape(self, shape_instance):
        self.shapes.append(shape_instance)

    def add_url(self, rule: str, view_class: PageView, view_name: str):
        view_class.set_shapes(self.shapes)

        self.app.add_url_rule(rule, view_func=view_class.as_view(view_name))

    def run(self):
        self.app.run()

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

    def compute_injected_css(self) -> List[str]:
        css = []

        for shape in self.shapes:
            for field in shape.fields:
                for css_item in field.injected_css:
                    css_item_full = "{css}.css".format(css=css_item)

                    if css.count(css_item_full) == 0:
                        css.append(css_item_full)

        return css

    def compute_injected_js(self) -> List[str]:
        js = []

        for shape in self.shapes:
            for field in shape.fields:
                for js_item in field.injected_js:
                    js_item_full = "{js}.js".format(js=js_item)

                    if js.count(js_item_full) == 0:
                        js.append(js_item_full)

        return js

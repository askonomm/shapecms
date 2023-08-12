from typing import List
from flask.views import MethodView
from shapecms import Shape


class PageView(MethodView):
    shapes: List[Shape] = []

    def set_shapes(self, shapes: List[Shape]):
        self.shapes = shapes

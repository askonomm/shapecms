from typing import List
from shapecms.shape_field import ShapeField


class Shape:
    """Class representing a Content Shape"""
    identifier: str = ""
    name: str = ""
    singular_name: str = ""
    admin_list_view_fields: List[str] = []
    fields: List[ShapeField] = []

    def set_identifier(self, identifier):
        self.identifier = identifier

    def add_field(self, field: ShapeField):
        self.fields.append(field)

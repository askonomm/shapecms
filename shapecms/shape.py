from typing import List
from shapecms.shape_field import ShapeField


class Shape:
    """Class representing a Shape"""
    identifier: str = ""
    name: str = ""
    singular_name: str = ""
    admin_list_view_fields: List[str] = []
    fields: List[ShapeField] = []

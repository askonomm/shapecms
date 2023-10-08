from typing import List, Self

from shapecms.fields.base import BaseField


class Shape:
    """Class representing a Content Shape"""

    identifier: str = ""
    name: str = ""
    singular_name: str = ""
    admin_list_view_fields: List[str] = []
    fields: List[BaseField] = []

    def __init__(self, **kwargs):
        if "identifier" in kwargs:
            self.identifier = kwargs.get("identifier")

        if "name" in kwargs:
            self.name = kwargs.get("name")

        if "singular_name" in kwargs:
            self.singular_name = kwargs.get("singular_name")

        if "admin_list_view_fields" in kwargs:
            self.admin_list_view_fields = kwargs.get("admin_list_view_fields")

        if "fields" in kwargs:
            self.fields = kwargs.get("fields")

    def __eq__(self, compared_to: Self):
        return self.identifier == compared_to.identifier

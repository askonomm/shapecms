from typing import List


class BaseField:
    """Class representing the base field"""

    identifier: str = ""
    name: str = ""
    output: str = ""
    admin_editable: callable = None
    admin_viewable: callable = None
    injected_css: List[str] = []
    injected_js: List[str] = []

    def __init__(self, **kwargs):
        if "identifier" in kwargs:
            self.identifier = kwargs.get("identifier")

        if "name" in kwargs:
            self.name = kwargs.get("name")

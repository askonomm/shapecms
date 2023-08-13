class ShapeField:
    """Class representing a Shape field"""
    identifier: str = ""
    name: str = ""
    admin_editable: callable = None
    admin_viewable: callable = None

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_name(self, name):
        self.name = name

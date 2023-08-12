class ShapeField:
    """Class representing a Shape field"""
    identifier: str = ""
    name: str = ""
    admin_editable: str = ""
    admin_viewable: str = ""

    def set_identifier(self, identifier):
        self.identifier = identifier

    def set_name(self, name):
        self.name = name

    def set_admin_editable(self, view):
        self.admin_editable = view

    def set_admin_viewable(self, view):
        self.admin_viewable = view

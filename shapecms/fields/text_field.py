from flask import render_template
from shapecms.shape_field import ShapeField


class TextField(ShapeField):
    placeholder: str = None
    prefix: str = None
    suffix: str = None

    def __init__(self):
        self.admin_editable = self._editable()
        self.admin_viewable = self._viewable()

    def _editable(self) -> callable:
        def view(value: str) -> str:
            context = {
                "placeholder": self.placeholder,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "value": value,
            }

            return render_template("fields/text/editable.html", **context)

        return view

    def _viewable(self) -> callable:
        def view(value: str) -> str:
            context = {
                "placeholder": self.placeholder,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "value": value,
            }

            return render_template("fields/text/viewable.html", **context)

        return view

    def set_placeholder(self, placeholder):
        self.placeholder = placeholder

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_suffix(self, suffix):
        self.suffix = suffix

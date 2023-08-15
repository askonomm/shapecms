from flask import render_template

from shapecms.fields.base import BaseField


class TextField(BaseField):
    placeholder: str = None
    prefix: str = None
    suffix: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.admin_editable = self._editable()
        self.admin_viewable = self._viewable()

        if "placeholder" in kwargs:
            self.placeholder = kwargs.get("placeholder")

        if "prefix" in kwargs:
            self.prefix = kwargs.get("prefix")

        if "suffix" in kwargs:
            self.suffix = kwargs.get("suffix")

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

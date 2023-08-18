from flask import render_template

from shapecms.fields.base import BaseField


class TextField(BaseField):
    placeholder: str = None
    prefix: str = None
    suffix: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.output = self.__output()
        self.admin_editable = self.__editable()
        self.admin_viewable = self.__viewable()
        self.injected_css = ["fields/text/text.css"]

        if "placeholder" in kwargs:
            self.placeholder = kwargs.get("placeholder")

        if "prefix" in kwargs:
            self.prefix = kwargs.get("prefix")

        if "suffix" in kwargs:
            self.suffix = kwargs.get("suffix")

    def __output(self) -> callable:
        """
        Returns a callable which transforms the field value into
        appropriate form.
        """

        def call(value: str | None) -> str:
            if value:
                return value

            return ""

        return call

    def __editable(self) -> callable:
        """
        Returns a callable which outputs an editable, self-updating
        field.
        """

        def view(content_id: str, value: str | None) -> str:
            if value is None:
                value = ""

            placeholder = ""

            if self.placeholder:
                placeholder = self.placeholder

            context = {
                "content_id": content_id,
                "identifier": self.identifier,
                "placeholder": placeholder,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "value": value,
            }

            return render_template("fields/text/editable.html", **context)

        return view

    def __viewable(self) -> callable:
        """
        Returns a callable which outputs a viewable field.
        """

        def view(value: str | None) -> str:
            if not value and self.placeholder:
                value = self.placeholder

            if not value and not self.placeholder:
                value = ""

            placeholder = ""

            if self.placeholder:
                placeholder = self.placeholder

            context = {
                "placeholder": placeholder,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "value": value,
            }

            return render_template("fields/text/viewable.html", **context)

        return view

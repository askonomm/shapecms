from typing import Any
from flask import redirect, render_template
from sqlalchemy import select
from sqlalchemy.orm import Session
from shapecms.db import ContentField
from shapecms.page_views import AdminPageView
from shapecms.shape import Shape


class ContentEditView(AdminPageView):
    current_shape: Shape = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __fields(self, content_id: int) -> list[dict[str, str | Any]]:
        """
        Given `content_id`, compose and return a list of editable fields
        for the content edit view.
        """
        result = []
        fields = self.current_shape.fields

        with Session(self.db) as s:
            for field in fields:
                stmt = (
                    select(ContentField)
                    .where(ContentField.content_id == content_id)
                    .where(ContentField.identifier == field.identifier)
                )

                field_data = s.execute(stmt).scalars().first()
                field_value = ""

                if field_data:
                    field_value = field_data.value

                result.append(
                    {
                        "name": field.name,
                        "identifier": field.identifier,
                        "editable": field.admin_editable(content_id, field_value),
                    }
                )

        return result

    def get(self, identifier: str, id: int):
        if not self.is_setup():
            return redirect("/admin/setup")

        if not self.is_authenticated():
            return redirect("/admin/login")

        self.current_shape = next(
            (x for x in self.shapes if x.identifier == identifier), None
        )

        if not self.current_shape:
            return redirect("/admin")

        context = {
            "shape_identifier": identifier,
            "fields": self.__fields(id),
            "injected_css": self.compute_injected_css(),
            "injected_js": self.compute_injected_js(),
        }

        return render_template("admin/content_edit.html", **context)

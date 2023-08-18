from typing import List
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

    def __fields(self, content_id: int) -> List[str]:
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

                field_value = s.execute(stmt).scalars().first()

                result.append({
                    "name": field.name,
                    "identifier": field.identifier,
                    "editable": field.admin_editable(field_value)
                })

        return result

    def get(self, identifier: str, id: int):
        self.current_shape = next(
            (x for x in self.shapes if x.identifier == identifier), None)

        if not self.current_shape:
            return redirect("/admin")

        context = {
            "shape_identifier": identifier,
            "fields": self.__fields(id)
        }

        return render_template("admin/content_edit.html", **context)

from typing import List

from flask import redirect, session, render_template
from sqlalchemy import select
from sqlalchemy.orm import Session

from shapecms import Shape
from shapecms.db import Content, ContentField
from shapecms.page_views import AdminPageView
from shapecms.util import is_setup, is_authenticated


class ContentView(AdminPageView):
    current_shape: Shape = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __get_field_identifiers_in_shape(self) -> List[str]:
        identifiers = []

        for field in self.current_shape.fields:
            if identifiers.count(field.identifier) == 0:
                identifiers.append(field.identifier)

        return identifiers
    
    def __realize_field_viewables(self, fields: List[dict]):
        pass

    def __get_content_items(self, shape_identifier: str):
        with Session(self.db) as s:
            items = []
            stmt = select(Content).where(Content.shape_identifier == shape_identifier)
            result = s.execute(stmt).scalars().all()

            print(result)

            for result_item in result:
                fields_stmt = select(ContentField).where(ContentField.content_id == result_item.id)
                fields = s.execute(fields_stmt).scalars().all()

                items.append({
                    "id": result_item.id,
                    "fields": filter(lambda x: self.__get_field_identifiers_in_shape().count(x.identifier), fields)
                })

            return items

    def get(self, identifier: str):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        self.current_shape = next((x for x in self.shapes if x.identifier == identifier), None)

        if not self.current_shape:
            return redirect("/admin")

        context = {
            "shape": self.current_shape,
            "items": self.__get_content_items(self.current_shape.identifier)
        }

        return render_template("admin/content.html", **context)

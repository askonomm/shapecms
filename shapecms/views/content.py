from typing import List

from flask import redirect, render_template
from sqlalchemy import select
from sqlalchemy.orm import Session

from shapecms import Shape
from shapecms.db import Content, ContentField
from shapecms.page_views import AdminPageView


class ContentView(AdminPageView):
    current_shape: Shape = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __list_view_viewables(self, s: Session, content_id: int) -> List[str]:
        """
        Given `content_id`, compose and return a list of viewable fields
        for the admin list view.
        """
        result = []
        admin_list_view_fields = self.current_shape.admin_list_view_fields

        for field in admin_list_view_fields:
            curr_fields = self.current_shape.fields
            field_instance = next(
                (x for x in curr_fields if x.identifier == field), None
            )

            stmt = (
                select(ContentField)
                .where(ContentField.content_id == content_id)
                .where(ContentField.identifier == field_instance.identifier)
            )

            field_data = s.execute(stmt).scalars().first()
            field_value = ""

            if field_data:
                field_value = field_data.value

            result.append(field_instance.admin_viewable(field_value))

        return result

    def __content_items(self, shape_identifier: str):
        """
        Given `shape_identifier`, compose and return a list of content items
        for the admin list view.

        In here the viewables of the list-view fields are already computed
        and added to the result.
        """
        with Session(self.db) as s:
            items = []
            stmt = select(Content).where(Content.shape_identifier == shape_identifier)
            result = s.execute(stmt).scalars().all()

            for result_item in result:
                items.append(
                    {
                        "id": result_item.id,
                        "viewables": self.__list_view_viewables(s, result_item.id),
                    }
                )

            return items

    def get(self, identifier: str):
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
            "shape": self.current_shape,
            "items": self.__content_items(self.current_shape.identifier),
            "injected_css": self.compute_injected_css(),
            "injected_js": self.compute_injected_js(),
        }

        return render_template("admin/content.html", **context)

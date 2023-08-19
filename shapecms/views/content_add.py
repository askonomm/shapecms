from flask import redirect
from sqlalchemy import insert
from sqlalchemy.orm import Session
from shapecms.db import Content
from shapecms.page_views import AdminPageView


class ContentAddView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, identifier: str):
        if not self.is_setup():
            return redirect("/admin/setup")

        if not self.is_authenticated():
            return redirect("/admin/login")

        current_shape = next(
            (x for x in self.shapes if x.identifier == identifier), None)

        if not current_shape:
            return redirect("/admin")

        with Session(self.db) as s:
            stmt = insert(Content).values(shape_identifier=identifier)
            id = s.execute(stmt).inserted_primary_key[0]

            s.commit()

            return redirect("/admin/content/{identifier}/edit/{id}".format(identifier=identifier, id=id))

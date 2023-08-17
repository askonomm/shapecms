from flask import redirect, session
from sqlalchemy import insert
from sqlalchemy.orm import Session
from shapecms.db import Content
from shapecms.page_views import AdminPageView
from shapecms.util import is_authenticated, is_setup


class ContentAddView(AdminPageView):
    def get(self, identifier: str):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        current_shape = next((x for x in self.shapes if x.identifier == identifier), None)

        if not current_shape:
            return redirect("/admin")
        
        with Session(self.db) as s:
            stmt = insert(Content).values(shape_identifier=identifier)
            id = s.execute(stmt).inserted_primary_key[0]
            
            s.commit()

            return redirect("/admin/content/{identifier}/edit/{id}".format(identifier=identifier,id=id))

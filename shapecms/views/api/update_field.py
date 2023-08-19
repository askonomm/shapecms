from flask import session, request
from sqlalchemy import select, insert, update
from shapecms import AdminPageView
from sqlalchemy.orm import Session

from shapecms.db import Content, ContentField
from shapecms.util import is_setup, is_authenticated


class APIUpdateFieldView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def post(self, content_id: str, f_id: str):
        if not is_setup(self.db):
            return {"error": "Shape CMS is not set up."}

        if not is_authenticated(self.db, session):
            return {"error": "You don't have permission to do this."}

        if f_id not in request.form:
            return {"error": "Form key has to be the field identifier."}

        value = request.form[f_id]

        with Session(self.db) as s:
            stmt = select(Content).where(Content.id == content_id)
            content_item = s.execute(stmt).scalars().first()
            field_exists = next(
                (x for x in content_item.fields if x.identifier == f_id), None
            )

            # If the field does not exist, create it
            if not field_exists:
                create_stmt = insert(ContentField).values(
                    content_id=content_id,
                    identifier=f_id,
                    value=value,
                )

                s.execute(create_stmt)
                s.commit()

            # And if it does, update it.
            else:
                update_stmt = (
                    update(ContentField)
                    .where(ContentField.content_id == content_id)
                    .where(ContentField.identifier == f_id)
                    .values(value=value)
                )

                s.execute(update_stmt)
                s.commit()

            return {"status": "ok"}

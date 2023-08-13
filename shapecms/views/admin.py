from flask import session, redirect
from shapecms.page_view import PageView, AdminPageView
from shapecms.util import is_authenticated, is_setup


class AdminView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        # todo: check for content shapes, redirect to one or show an error
        return "hello"

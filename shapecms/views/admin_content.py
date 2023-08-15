from flask import redirect, session

from shapecms.page_views import AdminPageView
from shapecms.util import is_setup, is_authenticated


class AdminView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        return "content..."

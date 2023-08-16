from flask import redirect, session, render_template

from shapecms.page_views import AdminPageView
from shapecms.util import is_setup, is_authenticated


class ContentView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self, identifier: str):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        curr_shape = next((x for x in self.shapes if x.identifier == identifier), None)

        if not curr_shape:
            return redirect("/admin")

        context = {
            "shape": curr_shape
        }

        return render_template("admin/content.html", **context)

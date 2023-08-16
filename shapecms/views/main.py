from flask import session, redirect, render_template

from shapecms.page_views import AdminPageView
from shapecms.util import is_authenticated, is_setup


class MainView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        if not is_authenticated(self.db, session):
            return redirect("/admin/login")

        # todo: check for content shapes, redirect to one or show an error
        if len(self.shapes) > 0:
            identifier = self.shapes[0].identifier
            return redirect("/admin/content/{identifier}".format(identifier=identifier))

        return render_template("admin/no_shapes_found.html")

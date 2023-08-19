from flask import redirect, render_template

from shapecms.page_views import AdminPageView


class MainView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not self.is_setup():
            return redirect("/admin/setup")

        if not self.is_authenticated():
            return redirect("/admin/login")

        # todo: check for content shapes, redirect to one or show an error
        if len(self.shapes) > 0:
            identifier = self.shapes[0].identifier
            return redirect("/admin/content/{identifier}".format(identifier=identifier))

        return render_template("admin/no_shapes_found.html")

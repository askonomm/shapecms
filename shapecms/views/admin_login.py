from flask import session, redirect, render_template
from shapecms.shape_view import PageView


class AdminLoginView(PageView):
    def get(self):
        return render_template("admin/login.html")

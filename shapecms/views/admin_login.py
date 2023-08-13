from flask import session, redirect, render_template
from shapecms.page_view import PageView, AdminPageView


class AdminLoginView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        return render_template("admin/login.html")

    def post(self):
        return "asd"

from flask import session, redirect
from shapecms.shape_view import PageView


class AdminView(PageView):
    def get(self):
        if 'auth_token' in session:
            return "hello"

        return redirect("/admin/login")

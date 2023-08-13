import bcrypt
from flask import redirect, render_template, request, flash
from sqlalchemy import insert, values
from sqlalchemy.orm import Session

from shapecms.db import User
from shapecms.page_view import AdminPageView
from shapecms.util import is_setup


class AdminSetupView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if is_setup(self.db):
            return redirect("/admin")

        return render_template("admin/setup.html")

    def post(self):
        if is_setup(self.db):
            return redirect("/admin")

        email = request.form["email"]

        if not email:
            flash("E-mail is required.")
            return redirect("/admin/setup")

        password = request.form["password"]

        if not password:
            flash("Password is required.")
            return render_template("admin/setup.html", email=email)

        password_encrypted = bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt())

        new_user = User(email=email, password=password_encrypted)

        with Session(self.db) as session:
            session.add(new_user)
            session.commit()

            flash("Account successfully created.")
            return redirect("/admin")

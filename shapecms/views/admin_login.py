from uuid import uuid4

import bcrypt
from flask import session, redirect, render_template, request, flash
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from shapecms.db import User
from shapecms.page_view import PageView, AdminPageView
from shapecms.util import is_setup


class AdminLoginView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        return render_template("admin/login.html")

    def post(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        email = request.form["email"]

        if not email:
            flash("E-mail is required.")
            return redirect("/admin/login")

        password = request.form["password"]

        if not password:
            flash("Password is required.")
            return render_template("admin/login.html", email=email)

        stmt = select(User).where(User.email == email)

        with Session(self.db) as s:
            result = s.execute(stmt).scalars().first()

            if result is None:
                flash("No account found with given e-mail.")
                return render_template("admin/login.html", email=email)

            if not bcrypt.checkpw(bytes(password, "utf-8"), result.password):
                flash("Incorrect password.")
                return render_template("admin/login.html", email=email)

        with Session(self.db) as s:
            auth_token = str(uuid4())

            update_user_stmt = update(User).where(User.email == email).values(auth_token=auth_token)
            s.execute(update_user_stmt)
            s.commit()

            session["auth_token"] = auth_token

            return redirect("/admin")

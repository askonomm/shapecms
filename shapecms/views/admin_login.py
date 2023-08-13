from uuid import uuid4
import bcrypt
from flask import session, redirect, render_template, request, flash
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from shapecms.db import User
from shapecms.page_view import AdminPageView
from shapecms.util import is_setup


class AdminLoginView(AdminPageView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get(self):
        if not is_setup(self.db):
            return redirect("/admin/setup")

        return render_template("admin/login.html")

    def post(self):
        """Attempts to authenticate the user and log them in."""
        if not is_setup(self.db):
            return redirect("/admin/setup")

        # Validate e-mail
        email = request.form["email"]

        if not email:
            flash("E-mail is required.")
            return redirect("/admin/login")

        password = request.form["password"]

        # Validate password
        if not password:
            flash("Password is required.")
            return render_template("admin/login.html", email=email)

        # Validate account and password
        with Session(self.db) as s:
            stmt = select(User).where(User.email == email)
            result = s.execute(stmt).scalars().first()

            if result is None:
                flash("No account found with given e-mail.")
                return render_template("admin/login.html", email=email)

            if not bcrypt.checkpw(password.encode("utf-8"), result.password.encode("utf-8")):
                flash("Incorrect password.")
                return render_template("admin/login.html", email=email)

        # Set authentication token
        with Session(self.db) as s:
            auth_token = str(uuid4())

            stmt = update(User).where(User.email == email).values(auth_token=auth_token)
            s.execute(stmt)
            s.commit()

            session["auth_token"] = auth_token

            return redirect("/admin")

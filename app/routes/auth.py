from app import db
from app.forms.registration import RegistrationForm
from app.models.user import User
from werkzeug.security import generate_password_hash
from flask import Blueprint, render_template, redirect, url_for, flash
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/registration", methods=["GET", "POST"])
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User).where(
                (User.username == form.username.data) |
                (User.email == form.email.data)
            )
        ).scalar_one_or_none()

        if existing_user:
            flash("Username or email already exists.", "error")
            return render_template("registration.html", form=form)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username or email already exists.", "error")
            return render_template("registration.html", form=form)

        return redirect(url_for("auth.registration_success"))
    return render_template("registration.html", form=form)

@auth_bp.route("/registr_success")
def registration_success():
    return render_template("registr_success.html")

# This file contains: profile page route configuration

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db;
from app.forms.profile import ProfileForm;
from app.models.user import User;

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        existing_user = db.session.execute(
            db.select(User).where(
                (
                    (User.username == form.username.data) |
                    (User.email == form.email.data)
                ) &
                (User.id != current_user.id)
            )
        ).scalar_one_or_none()

        if existing_user:
            flash("Username or email already exists.", "error")
            return render_template("profile.html", form=form)
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.profile"))
    return render_template("profile.html", form=form)
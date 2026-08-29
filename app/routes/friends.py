from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models.user import User
from app.models.friendship import Friendship


friends_bp = Blueprint(
    "friends",
    __name__,
    url_prefix="/friends"
)


@friends_bp.route("/", methods=["GET", "POST"])
@login_required
def friends():

    search_result = None

    # =========================
    # SEARCH USER
    # =========================

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        if username:

            search_result = db.session.execute(
                db.select(User).where(
                    User.username == username
                )
            ).scalar_one_or_none()

            if search_result is None:

                flash(
                    "User not found.",
                    "error"
                )

            elif search_result.id == current_user.id:

                flash(
                    "You cannot add yourself.",
                    "error"
                )

                search_result = None


    # =========================
    # INCOMING REQUESTS
    # =========================

    pending_requests = db.session.execute(

        db.select(Friendship).where(

            Friendship.receiver_id == current_user.id,

            Friendship.status == "PENDING"

        )

    ).scalars().all()


    # =========================
    # CURRENT FRIENDS
    # =========================

    friendships = db.session.execute(

        db.select(Friendship).where(

            (
                (Friendship.sender_id == current_user.id)
                |
                (Friendship.receiver_id == current_user.id)
            ),

            Friendship.status == "ACCEPTED"

        )

    ).scalars().all()


    friend_users = []

    for friendship in friendships:

        if friendship.sender_id == current_user.id:

            friend_users.append(
                friendship.receiver
            )

        else:

            friend_users.append(
                friendship.sender
            )


    return render_template(
        "friends.html",
        search_result=search_result,
        pending_requests=pending_requests,
        friends=friend_users
    )


# =========================
# SEND FRIEND REQUEST
# =========================

@friends_bp.route(
    "/send/<int:user_id>",
    methods=["POST"]
)
@login_required
def send_request(user_id):

    target_user = db.session.get(
        User,
        user_id
    )

    if target_user is None:

        return "User not found", 404


    if target_user.id == current_user.id:

        flash(
            "You cannot add yourself.",
            "error"
        )

        return redirect(
            url_for("friends.friends")
        )


    # Check both directions:
    #
    # ME → THEM
    # or
    # THEM → ME

    existing = db.session.execute(

        db.select(Friendship).where(

            (
                (
                    Friendship.sender_id == current_user.id
                )
                &
                (
                    Friendship.receiver_id == target_user.id
                )
            )

            |

            (
                (
                    Friendship.sender_id == target_user.id
                )
                &
                (
                    Friendship.receiver_id == current_user.id
                )
            )

        )

    ).scalar_one_or_none()


    if existing:

        if existing.status == "ACCEPTED":

            flash(
                "You are already friends.",
                "error"
            )

        else:

            flash(
                "A friend request already exists.",
                "error"
            )

        return redirect(
            url_for("friends.friends")
        )


    friendship = Friendship(

        sender_id=current_user.id,

        receiver_id=target_user.id,

        status="PENDING"
    )


    db.session.add(friendship)

    db.session.commit()


    flash(
        f"Friend request sent to {target_user.username}.",
        "success"
    )


    return redirect(
        url_for("friends.friends")
    )


# =========================
# ACCEPT REQUEST
# =========================

@friends_bp.route(
    "/accept/<int:request_id>",
    methods=["POST"]
)
@login_required
def accept_request(request_id):

    friendship = db.session.get(
        Friendship,
        request_id
    )


    if friendship is None:

        return "Request not found", 404


    if friendship.receiver_id != current_user.id:

        return "Access denied", 403


    if friendship.status != "PENDING":

        return "Request already processed", 400


    friendship.status = "ACCEPTED"

    db.session.commit()


    flash(
        f"You are now friends with {friendship.sender.username}.",
        "success"
    )


    return redirect(
        url_for("friends.friends")
    )


# =========================
# REJECT REQUEST
# =========================

@friends_bp.route(
    "/reject/<int:request_id>",
    methods=["POST"]
)
@login_required
def reject_request(request_id):

    friendship = db.session.get(
        Friendship,
        request_id
    )


    if friendship is None:

        return "Request not found", 404


    if friendship.receiver_id != current_user.id:

        return "Access denied", 403


    db.session.delete(friendship)

    db.session.commit()


    flash(
        "Friend request rejected.",
        "success"
    )


    return redirect(
        url_for("friends.friends")
    )
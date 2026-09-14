import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

#import for dotenv(s)
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

from app.models.goal import Goal;
from app.models.task import Task;
from app.models.friendship import Friendship
from app.models.proof import Proof;


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    return db.session.get(User, int(user_id))

def create_app(test_config=None):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="render_pages",
    )
    app.config["SECRET_KEY"] = "dev-secret-key"
    
    # Local SQLite database, stored in the Flask instance folder.
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trackmate-local.db"
    # Previous remote Supabase/PostgreSQL configuration:
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    app.config["PROOF_UPLOAD_FOLDER"] = os.path.join(
        app.static_folder, "uploads", "proofs"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.config["PROOF_UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @app.before_request
    def expire_overdue_tasks():

        # Ignore users who are not logged in
        if not current_user.is_authenticated:
            return

        now = datetime.now()

        # Find ACTIVE tasks belonging to this user
        # whose deadline has already passed
        expired_tasks = db.session.execute(
            db.select(Task)
            .join(Goal, Task.goal_id == Goal.id)
            .where(
                Goal.owner_id == current_user.id,
                Task.status == "ACTIVE",
                Task.deadline < now
            )
        ).scalars().all()

        # Nothing expired
        if not expired_tasks:
            return

        # Mark every expired task
        for task in expired_tasks:
            task.status = "EXPIRED"

        # -1 rating for each newly expired task
        current_user.rating -= len(expired_tasks)

        db.session.commit()
        
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp;
    from app.routes.goals import goals_bp;
    from app.routes.tasks import tasks_bp;
    from app.routes.friends import friends_bp
    from app.routes.proof import proof_bp;

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(friends_bp)
    app.register_blueprint(proof_bp)

    with app.app_context():
        from app.models.user import User
        # @login_manager.user_loader
        # def load_user(user_id):
        #     return db.session.get(User, int(user_id))
        db.create_all()

    return app

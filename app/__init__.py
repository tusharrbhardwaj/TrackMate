import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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

def create_app():
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="render_pages",
    )
    app.config["SECRET_KEY"] = "dev-secret-key"
    
    #Below line creates the same schema in postgres remote db instead of local sqlite
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp;
    from app.routes.goals import goals_bp;
    from app.routes.tasks import tasks_bp;
    from app.routes.friends import friends_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(goals_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(friends_bp)

    with app.app_context():
        from app.models.user import User
        # @login_manager.user_loader
        # def load_user(user_id):
        #     return db.session.get(User, int(user_id))
        db.create_all()

    return app

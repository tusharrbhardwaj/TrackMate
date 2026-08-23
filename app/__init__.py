from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
login_manager = LoginManager()
from app.models.goal import Goal;

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
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trackmate.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    from app.routes.auth import auth_bp
    from app.routes.profile import profile_bp
    from app.routes.goals import goals_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(goals_bp)

    with app.app_context():
        from app.models.user import User

        @login_manager.user_loader
        def load_user(user_id):
            return db.session.get(User, int(user_id))
        db.create_all()

    return app

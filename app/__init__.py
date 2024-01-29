from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import SECRET_KEY, DATABASE_URI
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'authet.login'
login_manager.login_message_category = 'info'
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    db.init_app(app)
    login_manager.init_app(app)

    ma.init_app(app)
    with app.app_context():
        from app.api import api_bp
        app.register_blueprint(api_bp, url_prefix='/api')
        from .swagger import swagger_bp
        app.register_blueprint(swagger_bp)
        from .master import master_bp
        app.register_blueprint(master_bp)

        from .user import user_bp
        app.register_blueprint(user_bp)

        from .todo import todo_bp
        app.register_blueprint(todo_bp)

        from .cookie import cookie_bp
        app.register_blueprint(cookie_bp)

        from .auth import authet_bp
        app.register_blueprint(authet_bp)

        from app.todo import views
    return app


app = create_app()
migrate = Migrate(app, db)

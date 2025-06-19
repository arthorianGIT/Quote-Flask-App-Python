from flask import Flask
from flask_login import LoginManager
from models import db, User

def create_app():
    app = Flask(__name__)
    login_manager = LoginManager(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
    app.config['SECRET_KEY'] = 'my_secret_key'
    db.init_app(app)

    from main import main_blueprint as main
    app.register_blueprint(main)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'error'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get_or_404(int(id))

    from auth import auth_blueprint as auth
    app.register_blueprint(auth)

    app.run(debug=True)

create_app()
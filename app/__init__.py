from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
from flask_mail import Mail

mail = Mail()
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from .routes.home_routes import home_bp
    app.register_blueprint(home_bp)
    from .routes.cart_routes import cart_bp
    app.register_blueprint(cart_bp)
    from .routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    from .routes.dashboard_routes import dashboard_bp
    app.register_blueprint(dashboard_bp)
    from .routes.product_routes import product_bp
    app.register_blueprint(product_bp)
    from .routes.koc_controller import koc_bp
    app.register_blueprint(koc_bp)
    from .routes.business_controller import business_bp
    app.register_blueprint(business_bp)


    db.init_app(app)  
    mail.init_app(app)


    return app

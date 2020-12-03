from flask import Flask

from src.conf import app_config
from src.ml.controller.TextController import txt_api
from src.ml.controller.ImageController import img_api
from src.ml.model import db, bcrypt

def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)
    # app configuration
    # app.config.from_object(app_config["test"])
    app.config.from_object(app_config[env_name])

    bcrypt.init_app(app)
    # db init
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(txt_api, url_prefix='/semantive/txt')
    app.register_blueprint(img_api, url_prefix='/semantive/img')

    @app.route('/', methods=['GET'])
    def index():
        """
        healthcheck
        """
        return 'Welcome to Semantive Service by Aleksandra Steliga'

    return app


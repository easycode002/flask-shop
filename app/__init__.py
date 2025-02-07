from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config.config import DevelopmentConfig

db = SQLAlchemy();
migrate = Migrate()

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    return app
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from celery import Celery
import os
from dotenv import load_dotenv
from .tasks import scan_broken_links, monitor_pages, detect_spam_content
from celery.schedules import crontab

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
celery = Celery(__name__, broker=os.getenv('CELERY_BROKER_URL'))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'default_secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    
    celery.conf.update(app.config)
    
    with app.app_context():
        from . import views, models
        db.create_all()
    
    return app
# app/__init__.py (Add the following lines at the end)


def create_celery_app(app):
    celery.conf.update(app.config)
    celery.conf.beat_schedule = {
        'scan-broken-links-every-day': {
            'task': 'app.tasks.scan_broken_links',
            'schedule': crontab(hour=0, minute=0),  # Daily at midnight
        },
        'detect-spam-content-every-hour': {
            'task': 'app.tasks.detect_spam_content',
            'schedule': crontab(minute=0, hour='*'),  # Every hour
        },
        # Add more scheduled tasks as needed
    }
    return celery

celery = create_celery_app(app)

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shush'
    
    CORS(app, origins=["http://127.0.0.1", "http://localhost"])
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    return app
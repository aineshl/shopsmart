from flask import Flask
from flask_cors import CORS  # Add this import

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'shush'
    
    CORS(app)
    
    from .views import views
    
    app.register_blueprint(views, url_prefix='/')
    return app
import os
from flask import Flask, session
from flask_session import Session

def create_app():
    # Determine the base directory (which is 'src')
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, 'templates'),
        static_folder=os.path.join(base_dir, 'static')
    )
    
    # Set up configuration
    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, 'data', 'uploads')
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600

    # Configure Flask-Session to store sessions in the filesystem
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_FILE_DIR'] = os.path.join(base_dir, 'data', 'session_files')
    os.makedirs(app.config['SESSION_FILE_DIR'], exist_ok=True)
    Session(app)
    
    # Register Blueprints
    from .routes import bp
    app.register_blueprint(bp)
    
    return app

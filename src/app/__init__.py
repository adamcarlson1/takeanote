from flask import Flask
import os

def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, '..', 'templates'),
        static_folder=os.path.join(base_dir, '..', 'static')
    )

    app.config['UPLOAD_FOLDER'] = os.path.join(base_dir, '..', 'data', 'uploads')
    app.secret_key = 'your_secret_key_here'  # Change this to a secure key

    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app

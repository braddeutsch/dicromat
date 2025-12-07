import os
from flask import Flask
from flask_cors import CORS
from config import config
from models import db
from routes import api_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    
    CORS(app, origins=app.config.get('CORS_ORIGINS', ['http://localhost:3000']))
    
    app.register_blueprint(api_bp)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)

from models import db
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import models after loading environment variables


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',
                                                      'mysql+pymysql://root:password@localhost/warehouse_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app)

    # Register blueprints
    from auth import auth_bp
    from products import products_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)

    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'Warehouse Management System API is running'}

    @app.route('/api/init-db')
    def init_db():
        try:
            db.create_all()
            return {'status': 'success', 'message': 'Database tables created successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

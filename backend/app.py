from models import db
from flask import Flask, jsonify
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
    CORS(app, supports_credentials=True, origins=['http://localhost:5173'])

    # Register blueprints
    from auth import auth_bp
    from products import products_bp
    from suppliers import suppliers_bp
    from customers import customers_bp
    from orders import orders_bp
    from inventory import inventory_bp
    from locations import locations_bp
    from shipments import shipments_bp
    from scrap import scrap_bp
    from users import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(suppliers_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(locations_bp)
    app.register_blueprint(shipments_bp)
    app.register_blueprint(scrap_bp)
    app.register_blueprint(users_bp)

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

    @app.route('/api/dashboard/stats')
    def get_dashboard_stats():
        """Get aggregated dashboard statistics"""
        try:
            from models import InventoryLot, Order, Scrap, Product, Location
            from sqlalchemy import func, and_
            from datetime import date, timedelta

            # Inventory stats
            total_inventory = db.session.query(
                func.sum(InventoryLot.quantity)).scalar() or 0

            low_stock_count = db.session.query(func.count(InventoryLot.product_id)).filter(
                InventoryLot.quantity <= 10
            ).scalar() or 0

            # Order stats
            pending_orders = Order.query.filter(
                Order.status == 'Pending').count()

            # Scrap stats (this month)
            today = date.today()
            month_start = date(today.year, today.month, 1)
            monthly_scrap = db.session.query(func.count(Scrap.scrap_id)).filter(
                Scrap.scrap_date >= month_start
            ).scalar() or 0

            return jsonify({
                'success': True,
                'data': {
                    'total_inventory': total_inventory,
                    'low_stock_count': low_stock_count,
                    'pending_orders': pending_orders,
                    'monthly_scrap': monthly_scrap
                }
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch dashboard statistics: {str(e)}'
            }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

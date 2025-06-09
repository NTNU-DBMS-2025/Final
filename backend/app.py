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

    # Simplified CORS configuration for development and production
    CORS(app,
         supports_credentials=True,
         origins=[
             'http://localhost:5173',  # Local frontend
             'http://localhost:3000',  # Alternative local port
             os.getenv('FRONTEND_URL', 'http://localhost:5173')
         ],
         allow_headers=['Content-Type', 'Authorization'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
         )

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
    from reports import reports_bp

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
    app.register_blueprint(reports_bp)

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
            from sqlalchemy import text

            # Use the same views as reports for consistency
            # Low stock items using the view
            low_stock_result = db.session.execute(
                text("SELECT COUNT(*) FROM v_low_stock"))
            low_stock_count = low_stock_result.scalar() or 0

            # Total inventory using a simple aggregate
            total_inventory_result = db.session.execute(
                text("SELECT COALESCE(SUM(quantity), 0) FROM Inventory_Lot"))
            total_inventory = total_inventory_result.scalar() or 0

            # Pending orders using the view
            pending_orders_result = db.session.execute(
                text("SELECT COUNT(*) FROM v_orders_pending"))
            pending_orders = pending_orders_result.scalar() or 0

            # Monthly scrap using the view
            scrap_result = db.session.execute(
                text("SELECT COALESCE(SUM(scrap_records), 0) FROM v_scrap_cost_month"))
            monthly_scrap = scrap_result.scalar() or 0

            return jsonify({
                'success': True,
                'data': {
                    'total_inventory': int(total_inventory),
                    'low_stock_count': int(low_stock_count),
                    'pending_orders': int(pending_orders),
                    'monthly_scrap': int(monthly_scrap)
                }
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch dashboard statistics: {str(e)}'
            }), 500

    @app.route('/api/dashboard/sales-stats')
    def get_sales_dashboard_stats():
        """Get aggregated sales dashboard statistics"""
        try:
            from models import InventoryLot, Order, Scrap, Product, Location, Customer
            from sqlalchemy import func, and_
            from datetime import date, timedelta, datetime

            # Today's date
            today = date.today()
            month_start = date(today.year, today.month, 1)

            # Today's orders count
            today_orders = Order.query.filter(
                func.date(Order.order_date) == today
            ).count()

            # Monthly revenue (sum of total_amount for this month)
            monthly_revenue = db.session.query(
                func.sum(Order.total_amount)
            ).filter(
                Order.order_date >= month_start
            ).scalar() or 0

            # Pending orders count
            pending_orders = Order.query.filter(
                Order.status == 'pending').count()

            # Total customers count
            total_customers = Customer.query.count()

            # Top customers by total order amount
            top_customers_data = db.session.query(
                Customer.customer_id,
                Customer.name,
                Customer.email,
                func.sum(Order.total_amount).label('total_amount'),
                func.count(Order.order_id).label('order_count')
            ).join(Order).group_by(Customer.customer_id)\
             .order_by(func.sum(Order.total_amount).desc()).limit(5).all()

            top_customers = [
                {
                    'id': stat[0],
                    'name': stat[1],
                    'email': stat[2] or 'No email',
                    'total_orders': float(stat[3]) if stat[3] else 0,
                    'order_count': stat[4]
                } for stat in top_customers_data
            ]

            return jsonify({
                'success': True,
                'data': {
                    'today_orders': today_orders,
                    'monthly_revenue': float(monthly_revenue),
                    'pending_orders': pending_orders,
                    'total_customers': total_customers,
                    'top_customers': top_customers
                }
            })

        except Exception as e:
            return jsonify({
                'success': False,
                'error': f'Failed to fetch sales dashboard statistics: {str(e)}'
            }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)

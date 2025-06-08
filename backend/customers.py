from flask import Blueprint, request, jsonify
from models import db, Customer, Order
from auth import require_auth, require_role
from sqlalchemy import func
from datetime import datetime, timedelta

customers_bp = Blueprint('customers', __name__, url_prefix='/api/customers')


@customers_bp.route('', methods=['GET'])
@require_auth
def get_customers():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')

        query = Customer.query

        if search:
            query = query.filter(
                Customer.name.contains(search) |
                Customer.contact.contains(search) |
                Customer.address.contains(search)
            )

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        customers = []
        for customer in pagination.items:
            customers.append(customer.to_dict())

        return jsonify({
            'success': True,
            'data': customers,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('/<int:customer_id>', methods=['GET'])
@require_auth
def get_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)

        # Get recent orders
        orders = []
        for order in customer.orders[:5]:  # Last 5 orders
            orders.append({
                'order_id': order.order_id,
                'order_date': order.order_date.isoformat(),
                'status': order.status,
                'ship_to': order.ship_to
            })

        customer_data = customer.to_dict()
        customer_data['total_orders'] = len(customer.orders)
        customer_data['recent_orders'] = orders

        return jsonify({
            'success': True,
            'data': customer_data
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('', methods=['POST'])
@require_role(['Admin', 'Sales'])
def create_customer():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400

        # Check if customer name already exists
        existing_customer = Customer.query.filter_by(name=data['name']).first()
        if existing_customer:
            return jsonify({'success': False, 'error': 'Customer name already exists'}), 400

        customer = Customer(
            name=data['name'],
            contact=data.get('contact'),
            phone=data.get('phone'),
            email=data.get('email'),
            address=data.get('address'),
            customer_type=data.get('customer_type', 'individual'),
            customer_level=data.get('customer_level', 'bronze'),
            tax_id=data.get('tax_id'),
            status=data.get('status', 'active'),
            notes=data.get('notes')
        )

        db.session.add(customer)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': customer.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@require_role(['Admin', 'Sales'])
def update_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)
        data = request.get_json()

        # Check if new customer name already exists (excluding current customer)
        if 'name' in data:
            existing_customer = Customer.query.filter(
                Customer.name == data['name'],
                Customer.customer_id != customer_id
            ).first()
            if existing_customer:
                return jsonify({'success': False, 'error': 'Customer name already exists'}), 400
            customer.name = data['name']

        if 'contact' in data:
            customer.contact = data['contact']

        if 'phone' in data:
            customer.phone = data['phone']

        if 'email' in data:
            customer.email = data['email']

        if 'address' in data:
            customer.address = data['address']

        if 'customer_type' in data:
            customer.customer_type = data['customer_type']

        if 'customer_level' in data:
            customer.customer_level = data['customer_level']

        if 'tax_id' in data:
            customer.tax_id = data['tax_id']

        if 'status' in data:
            customer.status = data['status']

        if 'notes' in data:
            customer.notes = data['notes']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': customer.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@require_role(['Admin'])
def delete_customer(customer_id):
    try:
        customer = Customer.query.get_or_404(customer_id)

        # Check if customer has orders
        if customer.orders:
            return jsonify({
                'success': False,
                'error': f'Cannot delete customer with {len(customer.orders)} existing orders'
            }), 400

        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Customer deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('/<int:customer_id>/orders', methods=['GET'])
@require_auth
def get_customer_orders(customer_id):
    """Get all orders for a specific customer"""
    try:
        customer = Customer.query.get_or_404(customer_id)

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        orders_query = Order.query.filter_by(customer_id=customer_id)
        pagination = orders_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        orders = []
        for order in pagination.items:
            orders.append({
                'order_id': order.order_id,
                'order_date': order.order_date.isoformat(),
                'status': order.status,
                'ship_to': order.ship_to,
                'user_name': order.user.account,
                'items_count': len(order.order_items)
            })

        return jsonify({
            'success': True,
            'data': {
                'customer': {
                    'customer_id': customer.customer_id,
                    'name': customer.name,
                    'contact': customer.contact,
                    'address': customer.address
                },
                'orders': orders,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total
                }
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@customers_bp.route('/stats', methods=['GET'])
@require_auth
def get_customer_stats():
    """Get customer statistics"""
    try:
        # Total customers
        total_customers = Customer.query.count()

        # Active customers
        active_customers = Customer.query.filter_by(status='active').count()

        # New customers this month
        today = datetime.now()
        month_start = datetime(today.year, today.month, 1)
        new_customers_month = Customer.query.filter(
            Customer.created_at >= month_start
        ).count()

        # Customer by type
        customer_by_type = db.session.query(
            Customer.customer_type,
            func.count(Customer.customer_id).label('count')
        ).group_by(Customer.customer_type).all()

        type_breakdown = {stat[0]: stat[1] for stat in customer_by_type}

        # Customer by level
        customer_by_level = db.session.query(
            Customer.customer_level,
            func.count(Customer.customer_id).label('count')
        ).group_by(Customer.customer_level).all()

        level_breakdown = {stat[0]: stat[1] for stat in customer_by_level}

        # Top customers by order count
        top_customers = db.session.query(
            Customer.customer_id,
            Customer.name,
            func.count(Order.order_id).label('count')
        ).join(Order).group_by(Customer.customer_id)\
         .order_by(func.count(Order.order_id).desc()).limit(5).all()

        top_customers_list = [
            {
                'customer_id': stat[0],
                'name': stat[1],
                'order_count': stat[2]
            } for stat in top_customers
        ]

        return jsonify({
            'success': True,
            'data': {
                'total_customers': total_customers,
                'active_customers': active_customers,
                'new_customers_month': new_customers_month,
                'customer_by_type': type_breakdown,
                'customer_by_level': level_breakdown,
                'top_customers': top_customers_list
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

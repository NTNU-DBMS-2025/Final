from flask import Blueprint, request, jsonify
from models import db, Customer, Order
from auth import require_auth, require_role

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
            customers.append({
                'customer_id': customer.customer_id,
                'name': customer.name,
                'contact': customer.contact,
                'address': customer.address,
                'orders_count': len(customer.orders),
                'latest_order_date': max([order.order_date for order in customer.orders], default=None)
            })

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

        return jsonify({
            'success': True,
            'data': {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'contact': customer.contact,
                'address': customer.address,
                'total_orders': len(customer.orders),
                'recent_orders': orders
            }
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
            address=data.get('address')
        )

        db.session.add(customer)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'contact': customer.contact,
                'address': customer.address
            }
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

        if 'address' in data:
            customer.address = data['address']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'customer_id': customer.customer_id,
                'name': customer.name,
                'contact': customer.contact,
                'address': customer.address
            }
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

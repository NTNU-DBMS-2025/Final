from flask import Blueprint, request, jsonify
from models import db, Order, OrderItem, Customer, User, Product, InventoryLot
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')


@orders_bp.route('', methods=['GET'])
def get_orders():
    """Get all orders with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        customer_filter = request.args.get('customer_id', type=int)
        search = request.args.get('search', '').strip()

        # Build query
        query = db.session.query(Order).join(Customer).join(User)

        # Apply filters
        if status_filter:
            query = query.filter(Order.status == status_filter)
        if customer_filter:
            query = query.filter(Order.customer_id == customer_filter)
        if search:
            query = query.filter(
                func.concat(Customer.name, ' ', Order.ship_to).contains(search)
            )

        # Order by most recent first
        query = query.order_by(Order.order_date.desc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        orders = []
        for order in pagination.items:
            # Calculate total items
            total_items = db.session.query(func.sum(OrderItem.quantity)).filter(
                OrderItem.order_id == order.order_id
            ).scalar() or 0

            # Get order items for frontend
            order_items = []
            for item in order.order_items:
                order_items.append({
                    'order_item_id': item.order_item_id,
                    'product_id': item.product_id,
                    'product_name': item.product.name if item.product else None,
                    'quantity': item.quantity,
                    'unit_price': float(item.unit_price) if hasattr(item, 'unit_price') and item.unit_price else 0.0
                })

            orders.append({
                'id': order.order_id,  # Frontend expects 'id'
                'order_id': order.order_id,
                'order_number': getattr(order, 'order_number', f'ORD{order.order_id:06d}'),
                'order_date': order.order_date.isoformat(),
                'order_date_raw': order.order_date.strftime('%Y-%m-%d'),
                'expected_delivery_date': getattr(order, 'expected_delivery_date', None),
                'status': order.status,
                'status_key': order.status.lower(),
                'priority': getattr(order, 'priority', 'normal'),
                'priority_key': getattr(order, 'priority', 'normal').lower(),
                'ship_to': order.ship_to,
                'total_amount': float(getattr(order, 'total_amount', 0.0)),
                'notes': getattr(order, 'notes', ''),
                'customer_id': order.customer_id,
                'customer_name': order.customer.name,
                'user_id': order.user_id,
                'sales_rep': order.user.account,
                'total_items': total_items,
                'order_items': order_items,
                'created_at': order.order_date.isoformat()
            })

        return jsonify({
            'success': True,
            'data': orders,
            'total': pagination.total,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch orders: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order with items"""
    try:
        order = Order.query.get_or_404(order_id)

        # Get order items with product details
        order_items = []
        for item in order.order_items:
            order_items.append({
                'order_item_id': item.order_item_id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'category': item.product.category,
                'quantity': item.quantity
            })

        return jsonify({
            'success': True,
            'data': {
                'order_id': order.order_id,
                'order_date': order.order_date.isoformat(),
                'status': order.status,
                'ship_to': order.ship_to,
                'customer_id': order.customer_id,
                'customer_name': order.customer.name,
                'customer_contact': order.customer.contact,
                'customer_address': order.customer.address,
                'user_id': order.user_id,
                'sales_rep': order.user.account,
                'order_items': order_items
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch order: {str(e)}'
        }), 500


@orders_bp.route('', methods=['POST'])
def create_order():
    """Create a new order with items"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['customer_id', 'user_id', 'ship_to', 'order_items']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate customer and user exist
        customer = Customer.query.get(data['customer_id'])
        if not customer:
            return jsonify({
                'success': False,
                'error': 'Customer not found'
            }), 404

        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        # Validate order items
        if not data['order_items'] or len(data['order_items']) == 0:
            return jsonify({
                'success': False,
                'error': 'Order must contain at least one item'
            }), 400

        # Check inventory availability for all items first
        for item_data in data['order_items']:
            product = Product.query.get(item_data['product_id'])
            if not product:
                return jsonify({
                    'success': False,
                    'error': f'Product not found: {item_data["product_id"]}'
                }), 404

            # Check total available inventory
            available_qty = db.session.query(func.sum(InventoryLot.quantity)).filter(
                InventoryLot.product_id == item_data['product_id']
            ).scalar() or 0

            if available_qty < item_data['quantity']:
                return jsonify({
                    'success': False,
                    'error': f'Insufficient inventory for {product.name}. Available: {available_qty}, Required: {item_data["quantity"]}'
                }), 400

        # Generate order number if not provided
        order_number = data.get('order_number')
        if not order_number:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            order_number = f"ORD{timestamp}"

        # Calculate total amount from order items
        total_amount = sum(
            item_data['quantity'] * item_data.get('unit_price', 0)
            for item_data in data['order_items']
        )

        # Create order with new fields
        order = Order(
            order_number=order_number,
            customer_id=data['customer_id'],
            user_id=data['user_id'],
            order_date=datetime.utcnow(),
            expected_delivery_date=data.get('expected_delivery_date'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'normal'),
            ship_to=data['ship_to'],
            total_amount=total_amount,
            notes=data.get('notes', '')
        )

        db.session.add(order)
        db.session.flush()  # Get order_id

        # Create order items and update inventory
        for item_data in data['order_items']:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                unit_price=item_data.get('unit_price', 0.0)
            )
            db.session.add(order_item)

            # Reduce inventory using FIFO (First In, First Out)
            remaining_qty = item_data['quantity']
            inventory_lots = InventoryLot.query.filter(
                InventoryLot.product_id == item_data['product_id'],
                InventoryLot.quantity > 0
            ).order_by(InventoryLot.expiry_date.asc()).all()

            for lot in inventory_lots:
                if remaining_qty <= 0:
                    break

                if lot.quantity >= remaining_qty:
                    lot.quantity -= remaining_qty
                    remaining_qty = 0
                else:
                    remaining_qty -= lot.quantity
                    lot.quantity = 0

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'data': {'order_id': order.order_id}
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Database integrity error'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to create order: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an existing order"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()

        # Update basic order information
        if 'status' in data:
            order.status = data['status']
        if 'ship_to' in data:
            order.ship_to = data['ship_to']
        if 'customer_id' in data:
            # Validate customer exists
            customer = Customer.query.get(data['customer_id'])
            if not customer:
                return jsonify({
                    'success': False,
                    'error': 'Customer not found'
                }), 404
            order.customer_id = data['customer_id']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update order: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order and its items (only if status allows)"""
    try:
        order = Order.query.get_or_404(order_id)

        # Only allow deletion if order is in draft or pending status
        if order.status not in ['Pending', 'Draft']:
            return jsonify({
                'success': False,
                'error': 'Cannot delete order with current status'
            }), 400

        # Restore inventory from order items before deletion
        for item in order.order_items:
            # Find the best location to restore inventory (first available location)
            location = InventoryLot.query.filter(
                InventoryLot.product_id == item.product_id
            ).first()

            if location:
                location.quantity += item.quantity
            else:
                # Create new inventory lot if none exists
                # Use first available location
                from models import Location
                first_location = Location.query.first()
                if first_location:
                    new_lot = InventoryLot(
                        product_id=item.product_id,
                        location_id=first_location.location_id,
                        quantity=item.quantity
                    )
                    db.session.add(new_lot)

        db.session.delete(order)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete order: {str(e)}'
        }), 500

# Order Items endpoints


@orders_bp.route('/<int:order_id>/items', methods=['GET'])
def get_order_items(order_id):
    """Get all items for a specific order"""
    try:
        order = Order.query.get_or_404(order_id)

        items = []
        for item in order.order_items:
            items.append({
                'order_item_id': item.order_item_id,
                'product_id': item.product_id,
                'product_name': item.product.name,
                'category': item.product.category,
                'quantity': item.quantity
            })

        return jsonify({
            'success': True,
            'data': items
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch order items: {str(e)}'
        }), 500


@orders_bp.route('/<int:order_id>/items', methods=['POST'])
def add_order_item(order_id):
    """Add an item to an existing order"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()

        # Validate required fields
        if 'product_id' not in data or 'quantity' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: product_id, quantity'
            }), 400

        # Validate product exists
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

        # Check inventory availability
        available_qty = db.session.query(func.sum(InventoryLot.quantity)).filter(
            InventoryLot.product_id == data['product_id']
        ).scalar() or 0

        if available_qty < data['quantity']:
            return jsonify({
                'success': False,
                'error': f'Insufficient inventory. Available: {available_qty}, Required: {data["quantity"]}'
            }), 400

        # Create order item
        order_item = OrderItem(
            order_id=order_id,
            product_id=data['product_id'],
            quantity=data['quantity']
        )

        db.session.add(order_item)

        # Update inventory using FIFO
        remaining_qty = data['quantity']
        inventory_lots = InventoryLot.query.filter(
            InventoryLot.product_id == data['product_id'],
            InventoryLot.quantity > 0
        ).order_by(InventoryLot.expiry_date.asc()).all()

        for lot in inventory_lots:
            if remaining_qty <= 0:
                break

            if lot.quantity >= remaining_qty:
                lot.quantity -= remaining_qty
                remaining_qty = 0
            else:
                remaining_qty -= lot.quantity
                lot.quantity = 0

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order item added successfully',
            'data': {'order_item_id': order_item.order_item_id}
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to add order item: {str(e)}'
        }), 500


@orders_bp.route('/items/<int:item_id>', methods=['DELETE'])
def delete_order_item(item_id):
    """Delete an order item"""
    try:
        item = OrderItem.query.get_or_404(item_id)

        # Restore inventory
        location = InventoryLot.query.filter(
            InventoryLot.product_id == item.product_id
        ).first()

        if location:
            location.quantity += item.quantity
        else:
            # Create new inventory lot if none exists
            from models import Location
            first_location = Location.query.first()
            if first_location:
                new_lot = InventoryLot(
                    product_id=item.product_id,
                    location_id=first_location.location_id,
                    quantity=item.quantity
                )
                db.session.add(new_lot)

        db.session.delete(item)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Order item deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete order item: {str(e)}'
        }), 500

# Statistics endpoints


@orders_bp.route('/stats', methods=['GET'])
def get_order_stats():
    """Get order statistics"""
    try:
        total_orders = Order.query.count()
        pending_orders = Order.query.filter(Order.status == 'Pending').count()
        shipped_orders = Order.query.filter(Order.status == 'Shipped').count()
        cancelled_orders = Order.query.filter(
            Order.status == 'Cancelled').count()

        # Recent orders (last 7 days)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_orders = Order.query.filter(
            Order.order_date >= week_ago).count()

        return jsonify({
            'success': True,
            'data': {
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'shipped_orders': shipped_orders,
                'cancelled_orders': cancelled_orders,
                'recent_orders': recent_orders
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch order statistics: {str(e)}'
        }), 500

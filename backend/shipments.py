from flask import Blueprint, request, jsonify
from models import db, Shipment, Order, ShippingVendor, User
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

shipments_bp = Blueprint('shipments', __name__, url_prefix='/api/shipments')


@shipments_bp.route('', methods=['GET'])
def get_shipments():
    """Get all shipments with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        vendor_filter = request.args.get('shipping_vendor_id', type=int)
        order_filter = request.args.get('order_id', type=int)
        search = request.args.get('search', '').strip()

        # Build query with joins
        query = db.session.query(Shipment).join(Order).join(ShippingVendor)

        # Apply filters
        if status_filter:
            query = query.filter(Shipment.status == status_filter)
        if vendor_filter:
            query = query.filter(Shipment.shipping_vendor_id == vendor_filter)
        if order_filter:
            query = query.filter(Shipment.order_id == order_filter)
        if search:
            query = query.filter(
                func.concat(Shipment.tracking_no, ' ',
                            ShippingVendor.name).contains(search)
            )

        # Order by most recent shipment date first
        query = query.order_by(Shipment.ship_date.desc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        shipments = []
        for shipment in pagination.items:
            shipments.append({
                'shipment_id': shipment.shipment_id,
                'ship_date': shipment.ship_date.isoformat(),
                'tracking_no': shipment.tracking_no,
                'tracking_number': shipment.tracking_no,  # Frontend compatibility
                'status': shipment.status,
                'estimated_shipping_date': getattr(shipment, 'estimated_shipping_date', None),
                'estimated_delivery_date': getattr(shipment, 'estimated_delivery_date', None),
                'actual_shipping_date': shipment.ship_date.strftime('%Y-%m-%d') if shipment.ship_date else None,
                'actual_delivery_date': getattr(shipment, 'actual_delivery_date', None),
                'shipping_address': getattr(shipment, 'shipping_address', None) or shipment.order.ship_to,
                'shipping_method': getattr(shipment, 'shipping_method', None) or shipment.shipping_vendor.mode,
                'notes': getattr(shipment, 'notes', ''),
                # Use order_number if available
                'order_id': getattr(shipment.order, 'order_number', shipment.order_id),
                'order_date': shipment.order.order_date.isoformat(),
                'customer_name': shipment.order.customer.name,
                'ship_to': shipment.order.ship_to,
                'shipping_vendor_id': shipment.shipping_vendor_id,
                'vendor_name': shipment.shipping_vendor.name,
                'shipping_mode': shipment.shipping_vendor.mode
            })

        return jsonify({
            'success': True,
            'data': shipments,
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
            'error': f'Failed to fetch shipments: {str(e)}'
        }), 500


@shipments_bp.route('/<int:shipment_id>', methods=['GET'])
def get_shipment(shipment_id):
    """Get a specific shipment with order details"""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)

        # Get order items
        order_items = []
        for item in shipment.order.order_items:
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
                'shipment_id': shipment.shipment_id,
                'ship_date': shipment.ship_date.isoformat(),
                'tracking_no': shipment.tracking_no,
                'status': shipment.status,
                'order_id': shipment.order_id,
                'order_date': shipment.order.order_date.isoformat(),
                'order_status': shipment.order.status,
                'customer_id': shipment.order.customer_id,
                'customer_name': shipment.order.customer.name,
                'customer_contact': shipment.order.customer.contact,
                'customer_address': shipment.order.customer.address,
                'ship_to': shipment.order.ship_to,
                'shipping_vendor_id': shipment.shipping_vendor_id,
                'vendor_name': shipment.shipping_vendor.name,
                'shipping_mode': shipment.shipping_vendor.mode,
                'order_items': order_items
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch shipment: {str(e)}'
        }), 500


@shipments_bp.route('', methods=['POST'])
def create_shipment():
    """Create a new shipment"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['order_id', 'shipping_vendor_id', 'tracking_no']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate order exists and is ready for shipping
        order = Order.query.get(data['order_id'])
        if not order:
            return jsonify({
                'success': False,
                'error': 'Order not found'
            }), 404

        if order.status in ['Cancelled', 'Shipped']:
            return jsonify({
                'success': False,
                'error': f'Cannot ship order with status: {order.status}'
            }), 400

        # Validate shipping vendor exists
        vendor = ShippingVendor.query.get(data['shipping_vendor_id'])
        if not vendor:
            return jsonify({
                'success': False,
                'error': 'Shipping vendor not found'
            }), 404

        # Parse ship date
        ship_date = datetime.utcnow()
        if 'ship_date' in data and data['ship_date']:
            try:
                ship_date = datetime.strptime(
                    data['ship_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    ship_date = datetime.strptime(
                        data['ship_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid ship date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS'
                    }), 400

        # Check if tracking number already exists
        existing_shipment = Shipment.query.filter(
            Shipment.tracking_no == data['tracking_no']
        ).first()

        if existing_shipment:
            return jsonify({
                'success': False,
                'error': 'Tracking number already exists'
            }), 400

        # Parse dates
        estimated_shipping_date = None
        if 'estimated_shipping_date' in data and data['estimated_shipping_date']:
            try:
                estimated_shipping_date = datetime.strptime(
                    data['estimated_shipping_date'], '%Y-%m-%d').date()
            except ValueError:
                pass

        estimated_delivery_date = None
        if 'estimated_delivery_date' in data and data['estimated_delivery_date']:
            try:
                estimated_delivery_date = datetime.strptime(
                    data['estimated_delivery_date'], '%Y-%m-%d').date()
            except ValueError:
                pass

        # Create shipment with new fields
        shipment = Shipment(
            order_id=data['order_id'],
            shipping_vendor_id=data['shipping_vendor_id'],
            tracking_no=data['tracking_no'],
            ship_date=ship_date,
            status=data.get('status', 'pending'),
            estimated_shipping_date=estimated_shipping_date,
            estimated_delivery_date=estimated_delivery_date,
            shipping_address=data.get('shipping_address', ''),
            shipping_method=data.get('shipping_method', ''),
            notes=data.get('notes', '')
        )

        db.session.add(shipment)

        # Update order status to Shipped
        order.status = 'Shipped'

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Shipment created successfully',
            'data': {
                'shipment_id': shipment.shipment_id,
                'tracking_no': shipment.tracking_no
            }
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
            'error': f'Failed to create shipment: {str(e)}'
        }), 500


@shipments_bp.route('/<int:shipment_id>', methods=['PUT'])
def update_shipment(shipment_id):
    """Update an existing shipment"""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)
        data = request.get_json()

        # Update status
        if 'status' in data:
            shipment.status = data['status']

            # If shipment is delivered, mark order as completed
            if data['status'] == 'Delivered':
                shipment.order.status = 'Completed'

        # Update tracking number
        if 'tracking_no' in data:
            # Check if new tracking number already exists
            existing_shipment = Shipment.query.filter(
                Shipment.tracking_no == data['tracking_no'],
                Shipment.shipment_id != shipment_id
            ).first()

            if existing_shipment:
                return jsonify({
                    'success': False,
                    'error': 'Tracking number already exists'
                }), 400

            shipment.tracking_no = data['tracking_no']

        # Update ship date
        if 'ship_date' in data and data['ship_date']:
            try:
                shipment.ship_date = datetime.strptime(
                    data['ship_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                try:
                    shipment.ship_date = datetime.strptime(
                        data['ship_date'], '%Y-%m-%d')
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid ship date format. Use YYYY-MM-DD or YYYY-MM-DD HH:MM:SS'
                    }), 400

        # Update shipping vendor
        if 'shipping_vendor_id' in data:
            vendor = ShippingVendor.query.get(data['shipping_vendor_id'])
            if not vendor:
                return jsonify({
                    'success': False,
                    'error': 'Shipping vendor not found'
                }), 404
            shipment.shipping_vendor_id = data['shipping_vendor_id']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Shipment updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update shipment: {str(e)}'
        }), 500


@shipments_bp.route('/<int:shipment_id>', methods=['DELETE'])
def delete_shipment(shipment_id):
    """Delete a shipment (only if not delivered)"""
    try:
        shipment = Shipment.query.get_or_404(shipment_id)

        # Only allow deletion if shipment is not delivered
        if shipment.status == 'Delivered':
            return jsonify({
                'success': False,
                'error': 'Cannot delete delivered shipment'
            }), 400

        # Revert order status back to confirmed/pending
        shipment.order.status = 'Confirmed'

        db.session.delete(shipment)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Shipment deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete shipment: {str(e)}'
        }), 500

# Shipping vendor management


@shipments_bp.route('/vendors', methods=['GET'])
def get_shipping_vendors():
    """Get all shipping vendors"""
    try:
        vendors = ShippingVendor.query.join(User).all()

        vendor_list = []
        for vendor in vendors:
            vendor_list.append({
                'user_id': vendor.user_id,
                'name': vendor.name,
                'mode': vendor.mode,
                'account': vendor.user.account
            })

        return jsonify({
            'success': True,
            'data': vendor_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch shipping vendors: {str(e)}'
        }), 500


@shipments_bp.route('/vendors', methods=['POST'])
def create_shipping_vendor():
    """Create a new shipping vendor"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['user_id', 'name', 'mode']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404

        # Check if vendor already exists for this user
        existing_vendor = ShippingVendor.query.get(data['user_id'])
        if existing_vendor:
            return jsonify({
                'success': False,
                'error': 'Shipping vendor already exists for this user'
            }), 400

        # Create shipping vendor
        vendor = ShippingVendor(
            user_id=data['user_id'],
            name=data['name'],
            mode=data['mode']
        )

        db.session.add(vendor)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Shipping vendor created successfully',
            'data': {
                'user_id': vendor.user_id,
                'name': vendor.name,
                'mode': vendor.mode
            }
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
            'error': f'Failed to create shipping vendor: {str(e)}'
        }), 500

# Analytics and tracking


@shipments_bp.route('/stats', methods=['GET'])
def get_shipment_stats():
    """Get shipment statistics"""
    try:
        total_shipments = Shipment.query.count()
        in_transit = Shipment.query.filter(
            Shipment.status == 'In Transit').count()
        delivered = Shipment.query.filter(
            Shipment.status == 'Delivered').count()
        delayed = Shipment.query.filter(Shipment.status == 'Delayed').count()

        # Recent shipments (last 7 days)
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_shipments = Shipment.query.filter(
            Shipment.ship_date >= week_ago).count()

        # Top shipping vendors
        vendor_stats = db.session.query(
            ShippingVendor.name,
            func.count(Shipment.shipment_id).label('shipment_count')
        ).join(Shipment).group_by(ShippingVendor.user_id, ShippingVendor.name)\
         .order_by(func.count(Shipment.shipment_id).desc()).limit(5).all()

        top_vendors = [{'name': stat[0], 'shipment_count': stat[1]}
                       for stat in vendor_stats]

        return jsonify({
            'success': True,
            'data': {
                'total_shipments': total_shipments,
                'in_transit': in_transit,
                'delivered': delivered,
                'delayed': delayed,
                'recent_shipments': recent_shipments,
                'top_vendors': top_vendors
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch shipment statistics: {str(e)}'
        }), 500


@shipments_bp.route('/track/<tracking_no>', methods=['GET'])
def track_shipment(tracking_no):
    """Track a shipment by tracking number"""
    try:
        shipment = Shipment.query.filter(
            Shipment.tracking_no == tracking_no).first()

        if not shipment:
            return jsonify({
                'success': False,
                'error': 'Shipment not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'tracking_no': shipment.tracking_no,
                'status': shipment.status,
                'ship_date': shipment.ship_date.isoformat(),
                'vendor_name': shipment.shipping_vendor.name,
                'shipping_mode': shipment.shipping_vendor.mode,
                'order_id': shipment.order_id,
                'customer_name': shipment.order.customer.name,
                'ship_to': shipment.order.ship_to
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to track shipment: {str(e)}'
        }), 500

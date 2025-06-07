from flask import Blueprint, request, jsonify
from models import db, InventoryLot, Product, Location
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError

inventory_bp = Blueprint('inventory', __name__, url_prefix='/api/inventory')


@inventory_bp.route('', methods=['GET'])
def get_inventory():
    """Get all inventory lots with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        product_filter = request.args.get('product_id', type=int)
        location_filter = request.args.get('location_id', type=int)
        zone_filter = request.args.get('zone', '').strip()
        low_stock = request.args.get('low_stock', type=bool)
        search = request.args.get('search', '').strip()

        # Build query with joins
        query = db.session.query(InventoryLot).join(Product).join(Location)

        # Apply filters
        if product_filter:
            query = query.filter(InventoryLot.product_id == product_filter)
        if location_filter:
            query = query.filter(InventoryLot.location_id == location_filter)
        if zone_filter:
            query = query.filter(Location.zone == zone_filter)
        if low_stock:
            # Consider low stock as quantity <= 10
            query = query.filter(InventoryLot.quantity <= 10)
        if search:
            query = query.filter(
                func.concat(Product.name, ' ', Location.zone,
                            ' ', Location.shelf).contains(search)
            )

        # Order by quantity (low stock first) then by expiry date
        query = query.order_by(InventoryLot.quantity.asc(),
                               InventoryLot.expiry_date.asc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        inventory_lots = []
        for lot in pagination.items:
            # Determine stock status
            stock_status = 'Good'
            if lot.quantity <= 5:
                stock_status = 'Critical'
            elif lot.quantity <= 10:
                stock_status = 'Low'

            # Check if expired or expiring soon
            expiry_status = 'Good'
            if lot.expiry_date:
                days_to_expiry = (lot.expiry_date - date.today()).days
                if days_to_expiry < 0:
                    expiry_status = 'Expired'
                elif days_to_expiry <= 7:
                    expiry_status = 'Expiring Soon'
                elif days_to_expiry <= 30:
                    expiry_status = 'Expiring'

            inventory_lots.append({
                'product_id': lot.product_id,
                'location_id': lot.location_id,
                'product_name': lot.product.name,
                'category': lot.product.category,
                'location_code': lot.location.location_code,
                'location_zone': lot.location.zone,
                'location_shelf': lot.location.shelf,
                'location_capacity': lot.location.capacity,
                'location_utilization_rate': lot.location.get_utilization_rate(),
                'quantity': lot.quantity,
                'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None,
                'stock_status': stock_status,
                'expiry_status': expiry_status
            })

        return jsonify({
            'success': True,
            'data': inventory_lots,
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
            'error': f'Failed to fetch inventory: {str(e)}'
        }), 500


@inventory_bp.route('/<int:product_id>/<int:location_id>', methods=['GET'])
def get_inventory_lot(product_id, location_id):
    """Get a specific inventory lot"""
    try:
        lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == product_id,
                 InventoryLot.location_id == location_id)
        ).first()

        if not lot:
            return jsonify({
                'success': False,
                'error': 'Inventory lot not found'
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'product_id': lot.product_id,
                'location_id': lot.location_id,
                'product_name': lot.product.name,
                'category': lot.product.category,
                'location_code': lot.location.location_code,
                'location_zone': lot.location.zone,
                'location_shelf': lot.location.shelf,
                'location_capacity': lot.location.capacity,
                'location_utilization_rate': lot.location.get_utilization_rate(),
                'quantity': lot.quantity,
                'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch inventory lot: {str(e)}'
        }), 500


@inventory_bp.route('', methods=['POST'])
def create_inventory_lot():
    """Create a new inventory lot (receiving goods)"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['product_id', 'location_id', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate product and location exist
        product = Product.query.get(data['product_id'])
        if not product:
            return jsonify({
                'success': False,
                'error': 'Product not found'
            }), 404

        location = Location.query.get(data['location_id'])
        if not location:
            return jsonify({
                'success': False,
                'error': 'Location not found'
            }), 404

        # Validate quantity
        if data['quantity'] <= 0:
            return jsonify({
                'success': False,
                'error': 'Quantity must be greater than 0'
            }), 400

        # Parse expiry date if provided
        expiry_date = None
        if 'expiry_date' in data and data['expiry_date']:
            try:
                expiry_date = datetime.strptime(
                    data['expiry_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid expiry date format. Use YYYY-MM-DD'
                }), 400

        # Check if inventory lot already exists for this product/location
        existing_lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == data['product_id'],
                 InventoryLot.location_id == data['location_id'])
        ).first()

        if existing_lot:
            # Update existing lot
            existing_lot.quantity += data['quantity']
            # Update expiry date if provided and it's earlier than existing
            if expiry_date and (not existing_lot.expiry_date or expiry_date < existing_lot.expiry_date):
                existing_lot.expiry_date = expiry_date

            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Inventory updated successfully',
                'data': {
                    'product_id': existing_lot.product_id,
                    'location_id': existing_lot.location_id,
                    'new_quantity': existing_lot.quantity
                }
            })
        else:
            # Create new inventory lot
            lot = InventoryLot(
                product_id=data['product_id'],
                location_id=data['location_id'],
                quantity=data['quantity'],
                expiry_date=expiry_date
            )

            db.session.add(lot)
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'Inventory lot created successfully',
                'data': {
                    'product_id': lot.product_id,
                    'location_id': lot.location_id,
                    'quantity': lot.quantity
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
            'error': f'Failed to create inventory lot: {str(e)}'
        }), 500


@inventory_bp.route('/<int:product_id>/<int:location_id>', methods=['PUT'])
def update_inventory_lot(product_id, location_id):
    """Update an existing inventory lot"""
    try:
        lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == product_id,
                 InventoryLot.location_id == location_id)
        ).first()

        if not lot:
            return jsonify({
                'success': False,
                'error': 'Inventory lot not found'
            }), 404

        data = request.get_json()

        # Update quantity
        if 'quantity' in data:
            if data['quantity'] < 0:
                return jsonify({
                    'success': False,
                    'error': 'Quantity cannot be negative'
                }), 400
            lot.quantity = data['quantity']

        # Update expiry date
        if 'expiry_date' in data:
            if data['expiry_date']:
                try:
                    lot.expiry_date = datetime.strptime(
                        data['expiry_date'], '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({
                        'success': False,
                        'error': 'Invalid expiry date format. Use YYYY-MM-DD'
                    }), 400
            else:
                lot.expiry_date = None

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Inventory lot updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update inventory lot: {str(e)}'
        }), 500


@inventory_bp.route('/<int:product_id>/<int:location_id>', methods=['DELETE'])
def delete_inventory_lot(product_id, location_id):
    """Delete an inventory lot"""
    try:
        lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == product_id,
                 InventoryLot.location_id == location_id)
        ).first()

        if not lot:
            return jsonify({
                'success': False,
                'error': 'Inventory lot not found'
            }), 404

        db.session.delete(lot)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Inventory lot deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete inventory lot: {str(e)}'
        }), 500

# Bulk operations


@inventory_bp.route('/bulk-update', methods=['POST'])
def bulk_update_inventory():
    """Bulk update multiple inventory lots"""
    try:
        data = request.get_json()

        if 'updates' not in data or not isinstance(data['updates'], list):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid updates array'
            }), 400

        updated_count = 0
        errors = []

        for update in data['updates']:
            try:
                lot = InventoryLot.query.filter(
                    and_(InventoryLot.product_id == update['product_id'],
                         InventoryLot.location_id == update['location_id'])
                ).first()

                if lot:
                    if 'quantity' in update:
                        lot.quantity = update['quantity']
                    if 'expiry_date' in update and update['expiry_date']:
                        lot.expiry_date = datetime.strptime(
                            update['expiry_date'], '%Y-%m-%d').date()
                    updated_count += 1
                else:
                    errors.append(
                        f"Lot not found: Product {update['product_id']}, Location {update['location_id']}")

            except Exception as e:
                errors.append(
                    f"Error updating Product {update['product_id']}, Location {update['location_id']}: {str(e)}")

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Bulk update completed. Updated {updated_count} lots.',
            'updated_count': updated_count,
            'errors': errors
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to perform bulk update: {str(e)}'
        }), 500

# Analytics and reports


@inventory_bp.route('/stats', methods=['GET'])
def get_inventory_stats():
    """Get inventory statistics"""
    try:
        # Total inventory value (count items)
        total_items = db.session.query(
            func.sum(InventoryLot.quantity)).scalar() or 0

        # Low stock items (quantity <= 10)
        low_stock_items = db.session.query(func.count(InventoryLot.product_id)).filter(
            InventoryLot.quantity <= 10
        ).scalar()

        # Critical stock items (quantity <= 5)
        critical_stock_items = db.session.query(func.count(InventoryLot.product_id)).filter(
            InventoryLot.quantity <= 5
        ).scalar()

        # Expired items
        today = date.today()
        expired_items = db.session.query(func.count(InventoryLot.product_id)).filter(
            InventoryLot.expiry_date < today
        ).scalar()

        # Expiring soon (next 7 days)
        week_ahead = today + timedelta(days=7)
        expiring_soon = db.session.query(func.count(InventoryLot.product_id)).filter(
            and_(InventoryLot.expiry_date >= today,
                 InventoryLot.expiry_date <= week_ahead)
        ).scalar()

        # Total unique products in inventory
        unique_products = db.session.query(func.count(
            func.distinct(InventoryLot.product_id))).scalar()

        # Total locations used
        used_locations = db.session.query(func.count(
            func.distinct(InventoryLot.location_id))).scalar()

        return jsonify({
            'success': True,
            'data': {
                'total_items': total_items,
                'unique_products': unique_products,
                'used_locations': used_locations,
                'low_stock_items': low_stock_items,
                'critical_stock_items': critical_stock_items,
                'expired_items': expired_items,
                'expiring_soon': expiring_soon
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch inventory statistics: {str(e)}'
        }), 500


@inventory_bp.route('/low-stock', methods=['GET'])
def get_low_stock_items():
    """Get items with low stock"""
    try:
        threshold = request.args.get('threshold', 10, type=int)

        low_stock_lots = db.session.query(InventoryLot).join(Product).join(Location).filter(
            InventoryLot.quantity <= threshold
        ).order_by(InventoryLot.quantity.asc()).all()

        items = []
        for lot in low_stock_lots:
            items.append({
                'product_id': lot.product_id,
                'product_name': lot.product.name,
                'category': lot.product.category,
                'location_id': lot.location_id,
                'location_zone': lot.location.zone,
                'location_shelf': lot.location.shelf,
                'quantity': lot.quantity,
                'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None
            })

        return jsonify({
            'success': True,
            'data': items,
            'count': len(items)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch low stock items: {str(e)}'
        }), 500


@inventory_bp.route('/expiring', methods=['GET'])
def get_expiring_items():
    """Get items that are expired or expiring soon"""
    try:
        days_ahead = request.args.get('days', 30, type=int)

        today = date.today()
        future_date = today + timedelta(days=days_ahead)

        expiring_lots = db.session.query(InventoryLot).join(Product).join(Location).filter(
            InventoryLot.expiry_date <= future_date
        ).order_by(InventoryLot.expiry_date.asc()).all()

        items = []
        for lot in expiring_lots:
            days_to_expiry = (lot.expiry_date -
                              today).days if lot.expiry_date else None

            status = 'Good'
            if days_to_expiry is not None:
                if days_to_expiry < 0:
                    status = 'Expired'
                elif days_to_expiry <= 7:
                    status = 'Expiring Soon'
                elif days_to_expiry <= 30:
                    status = 'Expiring'

            items.append({
                'product_id': lot.product_id,
                'product_name': lot.product.name,
                'category': lot.product.category,
                'location_id': lot.location_id,
                'location_zone': lot.location.zone,
                'location_shelf': lot.location.shelf,
                'quantity': lot.quantity,
                'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None,
                'days_to_expiry': days_to_expiry,
                'status': status
            })

        return jsonify({
            'success': True,
            'data': items,
            'count': len(items)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch expiring items: {str(e)}'
        }), 500

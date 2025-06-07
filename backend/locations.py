from flask import Blueprint, request, jsonify
from models import db, Location, InventoryLot, Product
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError

locations_bp = Blueprint('locations', __name__, url_prefix='/api/locations')


@locations_bp.route('', methods=['GET'])
def get_locations():
    """Get all locations with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        zone_filter = request.args.get('zone')
        search = request.args.get('search', '').strip()
        location_type_filter = request.args.get('location_type')
        status_filter = request.args.get('status')

        # Build query
        query = Location.query

        # Apply filters
        if zone_filter:
            query = query.filter(Location.zone == zone_filter)
        if location_type_filter:
            query = query.filter(Location.location_type ==
                                 location_type_filter)
        if status_filter:
            query = query.filter(Location.status == status_filter)
        if search:
            query = query.filter(
                or_(
                    Location.location_code.contains(search),
                    Location.location_name.contains(search),
                    Location.zone.contains(search),
                    Location.shelf.contains(search)
                )
            )

        # Order by zone, then shelf
        query = query.order_by(Location.zone.asc(), Location.shelf.asc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        locations = []
        for location in pagination.items:
            location_data = location.to_dict()
            locations.append(location_data)

        return jsonify({
            'success': True,
            'data': locations,
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
            'error': f'Failed to fetch locations: {str(e)}'
        }), 500


@locations_bp.route('/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """Get a specific location with inventory details"""
    try:
        location = Location.query.get_or_404(location_id)

        # Get inventory lots at this location
        inventory_lots = []
        for lot in location.inventory_lots:
            if lot.quantity > 0:  # Only show non-empty lots
                inventory_lots.append({
                    'product_id': lot.product_id,
                    'product_name': lot.product.name,
                    'category': lot.product.category,
                    'quantity': lot.quantity,
                    'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None
                })

        location_data = location.to_dict()
        location_data['inventory_lots'] = inventory_lots

        return jsonify({
            'success': True,
            'data': location_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch location: {str(e)}'
        }), 500


@locations_bp.route('', methods=['POST'])
def create_location():
    """Create a new storage location"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['location_code', 'location_name', 'zone', 'shelf']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Check if location code already exists
        existing_location = Location.query.filter(
            Location.location_code == data['location_code']
        ).first()

        if existing_location:
            return jsonify({
                'success': False,
                'error': 'Location with this code already exists'
            }), 400

        # Create new location
        location = Location(
            location_code=data['location_code'].strip(),
            location_name=data['location_name'].strip(),
            zone=data['zone'].strip(),
            shelf=data['shelf'].strip(),
            location_type=data.get('location_type', 'storage'),
            capacity=data.get('capacity', 0),
            status=data.get('status', 'active'),
            notes=data.get('notes', '')
        )

        db.session.add(location)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location created successfully',
            'data': location.to_dict()
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
            'error': f'Failed to create location: {str(e)}'
        }), 500


@locations_bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    """Update an existing location"""
    try:
        location = Location.query.get_or_404(location_id)
        data = request.get_json()

        # Update fields if provided
        if 'location_code' in data:
            # Check if new location code already exists (different location)
            existing = Location.query.filter(
                Location.location_code == data['location_code'],
                Location.location_id != location_id
            ).first()
            if existing:
                return jsonify({
                    'success': False,
                    'error': 'Location code already exists'
                }), 400
            location.location_code = data['location_code'].strip()

        if 'location_name' in data:
            location.location_name = data['location_name'].strip()
        if 'zone' in data:
            location.zone = data['zone'].strip()
        if 'shelf' in data:
            location.shelf = data['shelf'].strip()
        if 'location_type' in data:
            location.location_type = data['location_type']
        if 'capacity' in data:
            location.capacity = data['capacity']
        if 'status' in data:
            location.status = data['status']
        if 'notes' in data:
            location.notes = data['notes']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location updated successfully',
            'data': location.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update location: {str(e)}'
        }), 500


@locations_bp.route('/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """Delete a location (only if empty)"""
    try:
        location = Location.query.get_or_404(location_id)

        # Check if location has any inventory
        inventory_count = InventoryLot.query.filter(
            InventoryLot.location_id == location_id,
            InventoryLot.quantity > 0
        ).count()

        if inventory_count > 0:
            return jsonify({
                'success': False,
                'error': 'Cannot delete location with existing inventory. Please move or remove all items first.'
            }), 400

        # Delete all empty inventory lots first
        InventoryLot.query.filter(
            InventoryLot.location_id == location_id,
            InventoryLot.quantity == 0
        ).delete()

        db.session.delete(location)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete location: {str(e)}'
        }), 500


@locations_bp.route('/zones', methods=['GET'])
def get_zones():
    """Get all distinct zones with statistics"""
    try:
        zones = db.session.query(
            Location.zone).distinct().order_by(Location.zone).all()
        zone_list = [zone[0] for zone in zones]

        include_stats = request.args.get('include_stats', False, type=bool)
        if include_stats:
            zone_stats = []
            for zone_name in zone_list:
                location_count = Location.query.filter(
                    Location.zone == zone_name).count()

                # Total capacity in this zone
                total_capacity = db.session.query(func.sum(Location.capacity)).filter(
                    Location.zone == zone_name
                ).scalar() or 0

                # Total items in this zone
                total_items = db.session.query(func.sum(InventoryLot.quantity)).join(Location).filter(
                    Location.zone == zone_name
                ).scalar() or 0

                # Calculate utilization
                utilization_rate = (
                    total_items / total_capacity * 100) if total_capacity > 0 else 0

                zone_stats.append({
                    'zone': zone_name,
                    'location_count': location_count,
                    'total_capacity': total_capacity,
                    'total_items': total_items,
                    'utilization_rate': round(utilization_rate, 1)
                })

            return jsonify({
                'success': True,
                'data': zone_stats
            })
        else:
            return jsonify({
                'success': True,
                'data': zone_list
            })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch zones: {str(e)}'
        }), 500


@locations_bp.route('/types', methods=['GET'])
def get_location_types():
    """Get all available location types"""
    try:
        location_types = [
            {'value': 'storage', 'label': '一般儲存'},
            {'value': 'picking', 'label': '揀貨區'},
            {'value': 'receiving', 'label': '收貨區'},
            {'value': 'shipping', 'label': '出貨區'},
            {'value': 'staging', 'label': '暫存區'}
        ]

        return jsonify({
            'success': True,
            'data': location_types
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch location types: {str(e)}'
        }), 500


@locations_bp.route('/stats', methods=['GET'])
def get_location_stats():
    """Get overall location statistics"""
    try:
        # Total locations
        total_locations = Location.query.count()

        # Active locations
        active_locations = Location.query.filter(
            Location.status == 'active').count()

        # Total capacity
        total_capacity = db.session.query(
            func.sum(Location.capacity)).scalar() or 0

        # Total current stock
        total_stock = db.session.query(
            func.sum(InventoryLot.quantity)).scalar() or 0

        # Overall utilization
        overall_utilization = (
            total_stock / total_capacity * 100) if total_capacity > 0 else 0

        # Locations by status
        status_counts = db.session.query(
            Location.status, func.count(Location.location_id)
        ).group_by(Location.status).all()

        # Locations by type
        type_counts = db.session.query(
            Location.location_type, func.count(Location.location_id)
        ).group_by(Location.location_type).all()

        return jsonify({
            'success': True,
            'data': {
                'total_locations': total_locations,
                'active_locations': active_locations,
                'total_capacity': total_capacity,
                'total_stock': total_stock,
                'overall_utilization': round(overall_utilization, 1),
                'status_distribution': dict(status_counts),
                'type_distribution': dict(type_counts)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch location stats: {str(e)}'
        }), 500


@locations_bp.route('/<int:location_id>/inventory', methods=['GET'])
def get_location_inventory(location_id):
    """Get inventory at a specific location"""
    try:
        location = Location.query.get_or_404(location_id)

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        # Get inventory lots with product details
        inventory_query = db.session.query(InventoryLot, Product).join(Product).filter(
            InventoryLot.location_id == location_id,
            InventoryLot.quantity > 0
        ).order_by(Product.name)

        pagination = inventory_query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        inventory_items = []
        for lot, product in pagination.items:
            inventory_items.append({
                'product_id': product.product_id,
                'product_name': product.name,
                'category': product.category,
                'quantity': lot.quantity,
                'expiry_date': lot.expiry_date.isoformat() if lot.expiry_date else None,
                'warranty_years': product.warranty_years
            })

        return jsonify({
            'success': True,
            'data': {
                'location': location.to_dict(),
                'inventory': inventory_items,
                'pagination': {
                    'page': pagination.page,
                    'pages': pagination.pages,
                    'per_page': pagination.per_page,
                    'total': pagination.total,
                    'has_next': pagination.has_next,
                    'has_prev': pagination.has_prev
                }
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch location inventory: {str(e)}'
        }), 500


@locations_bp.route('/bulk-create', methods=['POST'])
def bulk_create_locations():
    """Create multiple locations at once"""
    try:
        data = request.get_json()

        if 'locations' not in data or not isinstance(data['locations'], list):
            return jsonify({
                'success': False,
                'error': 'Missing or invalid locations array'
            }), 400

        created_locations = []
        errors = []

        for loc_data in data['locations']:
            try:
                # Check required fields
                required_fields = ['location_code',
                                   'location_name', 'zone', 'shelf']
                for field in required_fields:
                    if field not in loc_data:
                        errors.append(
                            f"Missing {field} in location: {loc_data}")
                        continue

                # Check if location already exists
                existing = Location.query.filter(
                    Location.location_code == loc_data['location_code']
                ).first()

                if existing:
                    errors.append(
                        f"Location code {loc_data['location_code']} already exists")
                    continue

                # Create location
                location = Location(
                    location_code=loc_data['location_code'].strip(),
                    location_name=loc_data['location_name'].strip(),
                    zone=loc_data['zone'].strip(),
                    shelf=loc_data['shelf'].strip(),
                    location_type=loc_data.get('location_type', 'storage'),
                    capacity=loc_data.get('capacity', 0),
                    status=loc_data.get('status', 'active'),
                    notes=loc_data.get('notes', '')
                )

                db.session.add(location)
                created_locations.append(location)

            except Exception as e:
                errors.append(f"Error creating location {loc_data}: {str(e)}")

        if created_locations:
            db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Created {len(created_locations)} locations',
            'data': {
                'created_count': len(created_locations),
                'error_count': len(errors),
                'errors': errors
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to create locations: {str(e)}'
        }), 500

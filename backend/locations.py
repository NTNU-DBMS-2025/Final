from flask import Blueprint, request, jsonify
from models import db, Location, InventoryLot, Product
from sqlalchemy import func
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
        include_stats = request.args.get('include_stats', False, type=bool)

        # Build query
        query = Location.query

        # Apply filters
        if zone_filter:
            query = query.filter(Location.zone == zone_filter)
        if search:
            query = query.filter(
                func.concat(Location.zone, ' ',
                            Location.shelf).contains(search)
            )

        # Order by zone then shelf
        query = query.order_by(Location.zone.asc(), Location.shelf.asc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        locations = []
        for location in pagination.items:
            location_data = {
                'location_id': location.location_id,
                'zone': location.zone,
                'shelf': location.shelf
            }

            # Include inventory statistics if requested
            if include_stats:
                # Count unique products at this location
                unique_products = db.session.query(func.count(func.distinct(InventoryLot.product_id))).filter(
                    InventoryLot.location_id == location.location_id
                ).scalar() or 0

                # Total quantity at this location
                total_quantity = db.session.query(func.sum(InventoryLot.quantity)).filter(
                    InventoryLot.location_id == location.location_id
                ).scalar() or 0

                # Low stock items at this location (quantity <= 10)
                low_stock_items = db.session.query(func.count(InventoryLot.product_id)).filter(
                    InventoryLot.location_id == location.location_id,
                    InventoryLot.quantity <= 10
                ).scalar() or 0

                location_data.update({
                    'unique_products': unique_products,
                    'total_quantity': total_quantity,
                    'low_stock_items': low_stock_items,
                    'utilization': 'High' if unique_products > 5 else 'Medium' if unique_products > 0 else 'Empty'
                })

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

        # Calculate statistics
        total_quantity = sum(lot['quantity'] for lot in inventory_lots)
        unique_products = len(inventory_lots)

        return jsonify({
            'success': True,
            'data': {
                'location_id': location.location_id,
                'zone': location.zone,
                'shelf': location.shelf,
                'inventory_lots': inventory_lots,
                'stats': {
                    'unique_products': unique_products,
                    'total_quantity': total_quantity
                }
            }
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
        required_fields = ['zone', 'shelf']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Check if location already exists
        existing_location = Location.query.filter(
            Location.zone == data['zone'],
            Location.shelf == data['shelf']
        ).first()

        if existing_location:
            return jsonify({
                'success': False,
                'error': 'Location with this zone and shelf already exists'
            }), 400

        # Create new location
        location = Location(
            zone=data['zone'].strip(),
            shelf=data['shelf'].strip()
        )

        db.session.add(location)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location created successfully',
            'data': {
                'location_id': location.location_id,
                'zone': location.zone,
                'shelf': location.shelf
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
            'error': f'Failed to create location: {str(e)}'
        }), 500


@locations_bp.route('/<int:location_id>', methods=['PUT'])
def update_location(location_id):
    """Update an existing location"""
    try:
        location = Location.query.get_or_404(location_id)
        data = request.get_json()

        # Update zone if provided
        if 'zone' in data:
            location.zone = data['zone'].strip()

        # Update shelf if provided
        if 'shelf' in data:
            location.shelf = data['shelf'].strip()

        # Check for duplicates if zone or shelf changed
        if 'zone' in data or 'shelf' in data:
            existing_location = Location.query.filter(
                Location.zone == location.zone,
                Location.shelf == location.shelf,
                Location.location_id != location_id
            ).first()

            if existing_location:
                return jsonify({
                    'success': False,
                    'error': 'Location with this zone and shelf already exists'
                }), 400

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Location updated successfully'
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

# Zone management endpoints


@locations_bp.route('/zones', methods=['GET'])
def get_zones():
    """Get all distinct zones"""
    try:
        zones = db.session.query(
            Location.zone).distinct().order_by(Location.zone).all()
        zone_list = [zone[0] for zone in zones]

        # Get zone statistics if requested
        include_stats = request.args.get('include_stats', False, type=bool)
        if include_stats:
            zone_stats = []
            for zone_name in zone_list:
                location_count = Location.query.filter(
                    Location.zone == zone_name).count()

                # Total items in this zone
                total_items = db.session.query(func.sum(InventoryLot.quantity)).join(Location).filter(
                    Location.zone == zone_name
                ).scalar() or 0

                # Unique products in this zone
                unique_products = db.session.query(func.count(func.distinct(InventoryLot.product_id))).join(Location).filter(
                    Location.zone == zone_name
                ).scalar() or 0

                zone_stats.append({
                    'zone': zone_name,
                    'location_count': location_count,
                    'total_items': total_items,
                    'unique_products': unique_products
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


@locations_bp.route('/zones/<zone_name>', methods=['GET'])
def get_zone_locations(zone_name):
    """Get all locations in a specific zone"""
    try:
        locations = Location.query.filter(
            Location.zone == zone_name).order_by(Location.shelf).all()

        location_list = []
        for location in locations:
            # Get inventory summary for each location
            total_quantity = db.session.query(func.sum(InventoryLot.quantity)).filter(
                InventoryLot.location_id == location.location_id
            ).scalar() or 0

            unique_products = db.session.query(func.count(func.distinct(InventoryLot.product_id))).filter(
                InventoryLot.location_id == location.location_id,
                InventoryLot.quantity > 0
            ).scalar() or 0

            location_list.append({
                'location_id': location.location_id,
                'zone': location.zone,
                'shelf': location.shelf,
                'total_quantity': total_quantity,
                'unique_products': unique_products,
                'status': 'Empty' if total_quantity == 0 else 'Occupied'
            })

        return jsonify({
            'success': True,
            'data': location_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch zone locations: {str(e)}'
        }), 500

# Bulk operations


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
                if 'zone' not in loc_data or 'shelf' not in loc_data:
                    errors.append(
                        f"Missing zone or shelf in location data: {loc_data}")
                    continue

                # Check if location already exists
                existing = Location.query.filter(
                    Location.zone == loc_data['zone'],
                    Location.shelf == loc_data['shelf']
                ).first()

                if existing:
                    errors.append(
                        f"Location already exists: {loc_data['zone']}-{loc_data['shelf']}")
                    continue

                # Create new location
                location = Location(
                    zone=loc_data['zone'].strip(),
                    shelf=loc_data['shelf'].strip()
                )

                db.session.add(location)
                db.session.flush()  # Get ID

                created_locations.append({
                    'location_id': location.location_id,
                    'zone': location.zone,
                    'shelf': location.shelf
                })

            except Exception as e:
                errors.append(
                    f"Error creating location {loc_data.get('zone', '')}-{loc_data.get('shelf', '')}: {str(e)}")

        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Bulk creation completed. Created {len(created_locations)} locations.',
            'created_count': len(created_locations),
            'created_locations': created_locations,
            'errors': errors
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to perform bulk creation: {str(e)}'
        }), 500

# Analytics and reports


@locations_bp.route('/stats', methods=['GET'])
def get_location_stats():
    """Get location utilization statistics"""
    try:
        # Total locations
        total_locations = Location.query.count()

        # Occupied locations (have inventory)
        occupied_locations = db.session.query(func.count(func.distinct(InventoryLot.location_id))).filter(
            InventoryLot.quantity > 0
        ).scalar() or 0

        # Empty locations
        empty_locations = total_locations - occupied_locations

        # Total zones
        total_zones = db.session.query(func.count(
            func.distinct(Location.zone))).scalar() or 0

        # Location utilization percentage
        utilization_percentage = (
            occupied_locations / total_locations * 100) if total_locations > 0 else 0

        # Average items per location
        total_items = db.session.query(
            func.sum(InventoryLot.quantity)).scalar() or 0
        avg_items_per_location = total_items / \
            occupied_locations if occupied_locations > 0 else 0

        return jsonify({
            'success': True,
            'data': {
                'total_locations': total_locations,
                'occupied_locations': occupied_locations,
                'empty_locations': empty_locations,
                'total_zones': total_zones,
                'utilization_percentage': round(utilization_percentage, 2),
                'total_items': total_items,
                'avg_items_per_location': round(avg_items_per_location, 2)
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch location statistics: {str(e)}'
        }), 500


@locations_bp.route('/utilization', methods=['GET'])
def get_location_utilization():
    """Get detailed location utilization report"""
    try:
        # Get all locations with their utilization data
        locations_query = db.session.query(
            Location.location_id,
            Location.zone,
            Location.shelf,
            func.coalesce(func.sum(InventoryLot.quantity),
                          0).label('total_quantity'),
            func.count(InventoryLot.product_id).label('product_count')
        ).outerjoin(InventoryLot).group_by(
            Location.location_id, Location.zone, Location.shelf
        ).order_by(Location.zone, Location.shelf).all()

        utilization_data = []
        for loc in locations_query:
            status = 'Empty'
            if loc.total_quantity > 0:
                if loc.total_quantity > 100:
                    status = 'High'
                elif loc.total_quantity > 20:
                    status = 'Medium'
                else:
                    status = 'Low'

            utilization_data.append({
                'location_id': loc.location_id,
                'zone': loc.zone,
                'shelf': loc.shelf,
                'total_quantity': loc.total_quantity,
                'product_count': loc.product_count,
                'utilization_status': status
            })

        return jsonify({
            'success': True,
            'data': utilization_data
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch utilization report: {str(e)}'
        }), 500

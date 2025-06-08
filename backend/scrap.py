from flask import Blueprint, request, jsonify
from models import db, Scrap, Product, Location, InventoryLot
from datetime import datetime, date
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError

scrap_bp = Blueprint('scrap', __name__, url_prefix='/api/scrap')


@scrap_bp.route('', methods=['GET'])
def get_scrap_records():
    """Get all scrap records with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        product_filter = request.args.get('product_id', type=int)
        location_filter = request.args.get('location_id', type=int)
        search = request.args.get('search', '').strip()
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        # Build query with joins
        query = db.session.query(Scrap).join(Product).join(Location)

        # Apply filters
        if product_filter:
            query = query.filter(Scrap.product_id == product_filter)
        if location_filter:
            query = query.filter(Scrap.location_id == location_filter)
        if search:
            query = query.filter(
                func.concat(Product.name, ' ', Scrap.reason).contains(search)
            )

        # Date range filter
        if date_from:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                query = query.filter(Scrap.scrap_date >= from_date)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date_from format. Use YYYY-MM-DD'
                }), 400

        if date_to:
            try:
                to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                query = query.filter(Scrap.scrap_date <= to_date)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid date_to format. Use YYYY-MM-DD'
                }), 400

        # Order by most recent scrap date first
        query = query.order_by(Scrap.scrap_date.desc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        scrap_records = []
        for scrap in pagination.items:
            scrap_records.append(scrap.to_dict())

        return jsonify({
            'success': True,
            'data': scrap_records,
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
            'error': f'Failed to fetch scrap records: {str(e)}'
        }), 500


@scrap_bp.route('/<int:scrap_id>', methods=['GET'])
def get_scrap_record(scrap_id):
    """Get a specific scrap record"""
    try:
        scrap = Scrap.query.get_or_404(scrap_id)

        return jsonify({
            'success': True,
            'data': scrap.to_dict()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch scrap record: {str(e)}'
        }), 500


@scrap_bp.route('', methods=['POST'])
def create_scrap_record():
    """Create a new scrap record"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['product_id', 'location_id', 'quantity', 'reason']
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

        # Check if sufficient inventory exists at the location
        inventory_lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == data['product_id'],
                 InventoryLot.location_id == data['location_id'])
        ).first()

        if not inventory_lot or inventory_lot.quantity < data['quantity']:
            available_qty = inventory_lot.quantity if inventory_lot else 0
            return jsonify({
                'success': False,
                'error': f'Insufficient inventory at location. Available: {available_qty}, Required: {data["quantity"]}'
            }), 400

        # Parse scrap date
        scrap_date = date.today()
        if 'scrap_date' in data and data['scrap_date']:
            try:
                scrap_date = datetime.strptime(
                    data['scrap_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid scrap date format. Use YYYY-MM-DD'
                }), 400

        # Create scrap record
        scrap = Scrap(
            product_id=data['product_id'],
            location_id=data['location_id'],
            quantity=data['quantity'],
            scrap_date=scrap_date,
            reason=data['reason'].strip(),
            status=data.get('status', '待處理'),
            estimated_value=data.get('estimated_value', 0.0),
            description=data.get('description', ''),
            created_by=data.get('created_by', '')
        )

        db.session.add(scrap)

        # Reduce inventory quantity
        inventory_lot.quantity -= data['quantity']

        # If inventory quantity becomes 0, optionally keep the lot or delete it
        # For now, we'll keep it with 0 quantity for audit purposes

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Scrap record created successfully',
            'data': {
                'scrap_id': scrap.scrap_id,
                'remaining_inventory': inventory_lot.quantity
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
            'error': f'Failed to create scrap record: {str(e)}'
        }), 500


@scrap_bp.route('/<int:scrap_id>', methods=['PUT'])
def update_scrap_record(scrap_id):
    """Update an existing scrap record"""
    try:
        scrap = Scrap.query.get_or_404(scrap_id)
        data = request.get_json()

        # Store original quantity for inventory adjustment
        original_quantity = scrap.quantity

        # Update reason
        if 'reason' in data:
            scrap.reason = data['reason'].strip()

        # Update status
        if 'status' in data:
            scrap.status = data['status']
            # If status is being changed to '已處理', set processed_date
            if data['status'] == '已處理' and not scrap.processed_date:
                scrap.processed_date = date.today()

        # Update other fields
        if 'estimated_value' in data:
            scrap.estimated_value = data['estimated_value']

        if 'description' in data:
            scrap.description = data['description']

        if 'created_by' in data:
            scrap.created_by = data['created_by']

        # Update scrap date
        if 'scrap_date' in data and data['scrap_date']:
            try:
                scrap.scrap_date = datetime.strptime(
                    data['scrap_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': 'Invalid scrap date format. Use YYYY-MM-DD'
                }), 400

        # Update quantity (more complex as it affects inventory)
        if 'quantity' in data:
            if data['quantity'] <= 0:
                return jsonify({
                    'success': False,
                    'error': 'Quantity must be greater than 0'
                }), 400

            # Calculate the difference
            quantity_difference = data['quantity'] - original_quantity

            # Check if we have enough inventory for increase
            if quantity_difference > 0:
                inventory_lot = InventoryLot.query.filter(
                    and_(InventoryLot.product_id == scrap.product_id,
                         InventoryLot.location_id == scrap.location_id)
                ).first()

                if not inventory_lot or inventory_lot.quantity < quantity_difference:
                    available_qty = inventory_lot.quantity if inventory_lot else 0
                    return jsonify({
                        'success': False,
                        'error': f'Insufficient inventory for increase. Available: {available_qty}, Additional needed: {quantity_difference}'
                    }), 400

                # Reduce inventory
                inventory_lot.quantity -= quantity_difference
            elif quantity_difference < 0:
                # Increase inventory (returning scrapped items)
                inventory_lot = InventoryLot.query.filter(
                    and_(InventoryLot.product_id == scrap.product_id,
                         InventoryLot.location_id == scrap.location_id)
                ).first()

                if inventory_lot:
                    inventory_lot.quantity += abs(quantity_difference)
                else:
                    # Create new inventory lot
                    inventory_lot = InventoryLot(
                        product_id=scrap.product_id,
                        location_id=scrap.location_id,
                        quantity=abs(quantity_difference)
                    )
                    db.session.add(inventory_lot)

            scrap.quantity = data['quantity']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Scrap record updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update scrap record: {str(e)}'
        }), 500


@scrap_bp.route('/<int:scrap_id>', methods=['DELETE'])
def delete_scrap_record(scrap_id):
    """Delete a scrap record and restore inventory"""
    try:
        scrap = Scrap.query.get_or_404(scrap_id)

        # Restore inventory
        inventory_lot = InventoryLot.query.filter(
            and_(InventoryLot.product_id == scrap.product_id,
                 InventoryLot.location_id == scrap.location_id)
        ).first()

        if inventory_lot:
            inventory_lot.quantity += scrap.quantity
        else:
            # Create new inventory lot if it doesn't exist
            inventory_lot = InventoryLot(
                product_id=scrap.product_id,
                location_id=scrap.location_id,
                quantity=scrap.quantity
            )
            db.session.add(inventory_lot)

        db.session.delete(scrap)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Scrap record deleted and inventory restored successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete scrap record: {str(e)}'
        }), 500

# Process scrap record (change status)


@scrap_bp.route('/<int:scrap_id>/process', methods=['PUT'])
def process_scrap_record(scrap_id):
    """Process a scrap record (change status to 已處理)"""
    try:
        scrap = Scrap.query.get_or_404(scrap_id)

        if scrap.status == '已處理':
            return jsonify({
                'success': False,
                'error': 'Scrap record is already processed'
            }), 400

        scrap.status = '已處理'
        scrap.processed_date = date.today()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Scrap record processed successfully',
            'data': scrap.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to process scrap record: {str(e)}'
        }), 500

# Analytics and reports


@scrap_bp.route('/stats', methods=['GET'])
def get_scrap_stats():
    """Get scrap statistics"""
    try:
        # Total scrapped items
        total_scrapped = db.session.query(
            func.sum(Scrap.quantity)).scalar() or 0

        # Total scrap records
        total_records = Scrap.query.count()

        # Scrap by category
        category_stats = db.session.query(
            Product.category,
            func.sum(Scrap.quantity).label('total_scrapped'),
            func.count(Scrap.scrap_id).label('record_count')
        ).join(Product).group_by(Product.category)\
         .order_by(func.sum(Scrap.quantity).desc()).all()

        category_breakdown = [
            {
                'category': stat[0],
                'total_scrapped': stat[1],
                'record_count': stat[2]
            } for stat in category_stats
        ]

        # Recent scrap (last 30 days)
        from datetime import timedelta
        thirty_days_ago = date.today() - timedelta(days=30)
        recent_scrap = db.session.query(func.sum(Scrap.quantity)).filter(
            Scrap.scrap_date >= thirty_days_ago
        ).scalar() or 0

        # This month's scrap count
        today = date.today()
        month_start = date(today.year, today.month, 1)
        monthly_scrap = db.session.query(func.count(Scrap.scrap_id)).filter(
            Scrap.scrap_date >= month_start
        ).scalar() or 0

        # Status-based counts
        pending_count = Scrap.query.filter_by(status='待處理').count()
        processing_count = Scrap.query.filter_by(status='處理中').count()
        processed_count = Scrap.query.filter_by(status='已處理').count()

        # Total estimated value
        total_estimated_value = db.session.query(
            func.sum(Scrap.estimated_value)).scalar() or 0

        # Top scrap reasons
        reason_stats = db.session.query(
            Scrap.reason,
            func.sum(Scrap.quantity).label('total_quantity'),
            func.count(Scrap.scrap_id).label('record_count')
        ).group_by(Scrap.reason)\
         .order_by(func.sum(Scrap.quantity).desc()).limit(10).all()

        top_reasons = [
            {
                'reason': stat[0],
                'total_quantity': stat[1],
                'record_count': stat[2]
            } for stat in reason_stats
        ]

        # Scrap rate by location
        location_stats = db.session.query(
            Location.zone,
            Location.shelf,
            func.sum(Scrap.quantity).label('total_scrapped')
        ).join(Location).group_by(Location.location_id, Location.zone, Location.shelf)\
         .order_by(func.sum(Scrap.quantity).desc()).limit(10).all()

        top_locations = [
            {
                'zone': stat[0],
                'shelf': stat[1],
                'total_scrapped': stat[2]
            } for stat in location_stats
        ]

        return jsonify({
            'success': True,
            'data': {
                'total_scrapped': total_scrapped,
                'total_records': total_records,
                'recent_scrap_30days': recent_scrap,
                'monthly_scrap': monthly_scrap,
                'pending_count': pending_count,
                'processing_count': processing_count,
                'processed_count': processed_count,
                'total_estimated_value': float(total_estimated_value),
                'category_breakdown': category_breakdown,
                'top_reasons': top_reasons,
                'top_locations': top_locations
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch scrap statistics: {str(e)}'
        }), 500


@scrap_bp.route('/reasons', methods=['GET'])
def get_scrap_reasons():
    """Get distinct scrap reasons"""
    try:
        reasons = db.session.query(
            Scrap.reason).distinct().order_by(Scrap.reason).all()
        reason_list = [reason[0] for reason in reasons]

        return jsonify({
            'success': True,
            'data': reason_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch scrap reasons: {str(e)}'
        }), 500


@scrap_bp.route('/monthly-report', methods=['GET'])
def get_monthly_scrap_report():
    """Get monthly scrap report"""
    try:
        # Get year and month from query params
        year = request.args.get('year', datetime.now().year, type=int)
        month = request.args.get('month', datetime.now().month, type=int)

        # Validate month
        if month < 1 or month > 12:
            return jsonify({
                'success': False,
                'error': 'Month must be between 1 and 12'
            }), 400

        # Calculate date range for the month
        from calendar import monthrange
        start_date = date(year, month, 1)
        end_date = date(year, month, monthrange(year, month)[1])

        # Get scrap records for the month
        monthly_scrap = db.session.query(Scrap).join(Product).join(Location).filter(
            and_(Scrap.scrap_date >= start_date, Scrap.scrap_date <= end_date)
        ).all()

        # Calculate totals
        total_quantity = sum(record.quantity for record in monthly_scrap)
        total_records = len(monthly_scrap)

        # Group by product
        product_breakdown = {}
        for record in monthly_scrap:
            product_name = record.product.name
            if product_name not in product_breakdown:
                product_breakdown[product_name] = {
                    'product_id': record.product_id,
                    'category': record.product.category,
                    'total_quantity': 0,
                    'record_count': 0
                }
            product_breakdown[product_name]['total_quantity'] += record.quantity
            product_breakdown[product_name]['record_count'] += 1

        # Group by reason
        reason_breakdown = {}
        for record in monthly_scrap:
            reason = record.reason
            if reason not in reason_breakdown:
                reason_breakdown[reason] = 0
            reason_breakdown[reason] += record.quantity

        return jsonify({
            'success': True,
            'data': {
                'year': year,
                'month': month,
                'total_quantity': total_quantity,
                'total_records': total_records,
                'product_breakdown': product_breakdown,
                'reason_breakdown': reason_breakdown,
                'records': [
                    {
                        'scrap_id': record.scrap_id,
                        'product_name': record.product.name,
                        'location': f"{record.location.zone}-{record.location.shelf}",
                        'quantity': record.quantity,
                        'scrap_date': record.scrap_date.isoformat(),
                        'reason': record.reason
                    } for record in monthly_scrap
                ]
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to generate monthly scrap report: {str(e)}'
        }), 500

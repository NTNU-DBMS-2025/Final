from flask import Blueprint, request, jsonify
from models import db, Supplier, Product, supplier_product
from auth import require_auth, require_role

suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/api/suppliers')


@suppliers_bp.route('', methods=['GET'])
@require_auth
def get_suppliers():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')

        query = Supplier.query

        if search:
            query = query.filter(
                Supplier.supplier_name.contains(search) |
                Supplier.contact.contains(search)
            )

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        suppliers = []
        for supplier in pagination.items:
            suppliers.append({
                'supplier_id': supplier.supplier_id,
                'supplier_name': supplier.supplier_name,
                'contact': supplier.contact,
                'products_count': len(supplier.products),
                'products': [{'product_id': p.product_id, 'name': p.name}
                             for p in supplier.products]
            })

        return jsonify({
            'success': True,
            'data': suppliers,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>', methods=['GET'])
@require_auth
def get_supplier(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)

        return jsonify({
            'success': True,
            'data': {
                'supplier_id': supplier.supplier_id,
                'supplier_name': supplier.supplier_name,
                'contact': supplier.contact,
                'products': [{'product_id': p.product_id, 'name': p.name, 'category': p.category}
                             for p in supplier.products]
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('', methods=['POST'])
@require_role(['Admin', 'Warehouse'])
def create_supplier():
    try:
        data = request.get_json()

        # Validate required fields
        if 'supplier_name' not in data:
            return jsonify({'success': False, 'error': 'supplier_name is required'}), 400

        # Check if supplier name already exists
        existing_supplier = Supplier.query.filter_by(
            supplier_name=data['supplier_name']).first()
        if existing_supplier:
            return jsonify({'success': False, 'error': 'Supplier name already exists'}), 400

        supplier = Supplier(
            supplier_name=data['supplier_name'],
            contact=data.get('contact')
        )

        db.session.add(supplier)
        db.session.commit()

        # Add products if provided
        if 'product_ids' in data:
            for product_id in data['product_ids']:
                product = Product.query.get(product_id)
                if product:
                    supplier.products.append(product)
            db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'supplier_id': supplier.supplier_id,
                'supplier_name': supplier.supplier_name,
                'contact': supplier.contact,
                'products': [{'product_id': p.product_id, 'name': p.name}
                             for p in supplier.products]
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>', methods=['PUT'])
@require_role(['Admin', 'Warehouse'])
def update_supplier(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        data = request.get_json()

        # Check if new supplier name already exists (excluding current supplier)
        if 'supplier_name' in data:
            existing_supplier = Supplier.query.filter(
                Supplier.supplier_name == data['supplier_name'],
                Supplier.supplier_id != supplier_id
            ).first()
            if existing_supplier:
                return jsonify({'success': False, 'error': 'Supplier name already exists'}), 400
            supplier.supplier_name = data['supplier_name']

        if 'contact' in data:
            supplier.contact = data['contact']

        # Update products if provided
        if 'product_ids' in data:
            # Clear existing products
            supplier.products.clear()
            # Add new products
            for product_id in data['product_ids']:
                product = Product.query.get(product_id)
                if product:
                    supplier.products.append(product)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'supplier_id': supplier.supplier_id,
                'supplier_name': supplier.supplier_name,
                'contact': supplier.contact,
                'products': [{'product_id': p.product_id, 'name': p.name, 'category': p.category}
                             for p in supplier.products]
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>', methods=['DELETE'])
@require_role(['Admin'])
def delete_supplier(supplier_id):
    try:
        supplier = Supplier.query.get_or_404(supplier_id)

        # Check if supplier has products (you might want to prevent deletion)
        if supplier.products:
            return jsonify({
                'success': False,
                'error': f'Cannot delete supplier with {len(supplier.products)} associated products. Remove products first.'
            }), 400

        db.session.delete(supplier)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Supplier deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>/products', methods=['GET'])
@require_auth
def get_supplier_products(supplier_id):
    """Get all products for a specific supplier"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)

        products = []
        for product in supplier.products:
            products.append({
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'warranty_years': product.warranty_years,
                'image_url': product.image_url
            })

        return jsonify({
            'success': True,
            'data': {
                'supplier': {
                    'supplier_id': supplier.supplier_id,
                    'supplier_name': supplier.supplier_name,
                    'contact': supplier.contact
                },
                'products': products
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>/products/<int:product_id>', methods=['POST'])
@require_role(['Admin', 'Warehouse'])
def add_supplier_product(supplier_id, product_id):
    """Add a product to a supplier"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        product = Product.query.get_or_404(product_id)

        if product in supplier.products:
            return jsonify({'success': False, 'error': 'Product already associated with this supplier'}), 400

        supplier.products.append(product)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Product "{product.name}" added to supplier "{supplier.supplier_name}"'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@suppliers_bp.route('/<int:supplier_id>/products/<int:product_id>', methods=['DELETE'])
@require_role(['Admin', 'Warehouse'])
def remove_supplier_product(supplier_id, product_id):
    """Remove a product from a supplier"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        product = Product.query.get_or_404(product_id)

        if product not in supplier.products:
            return jsonify({'success': False, 'error': 'Product not associated with this supplier'}), 400

        supplier.products.remove(product)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': f'Product "{product.name}" removed from supplier "{supplier.supplier_name}"'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

from flask import Blueprint, request, jsonify
from models import db, Product, Supplier, supplier_product
from auth import require_auth, require_role

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


@products_bp.route('', methods=['GET'])
@require_auth
def get_products():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')

        query = Product.query

        if search:
            query = query.filter(
                Product.name.contains(search) |
                Product.category.contains(search)
            )

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )

        products = []
        for product in pagination.items:
            products.append({
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'warranty_years': product.warranty_years,
                'image_url': product.image_url,
                'suppliers': [{'supplier_id': s.supplier_id, 'supplier_name': s.supplier_name}
                            for s in product.suppliers]
            })

        return jsonify({
            'success': True,
            'data': products,
            'pagination': {
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['GET'])
@require_auth
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        return jsonify({
            'success': True,
            'data': {
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'warranty_years': product.warranty_years,
                'image_url': product.image_url,
                'suppliers': [{'supplier_id': s.supplier_id, 'supplier_name': s.supplier_name}
                              for s in product.suppliers]
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@products_bp.route('', methods=['POST'])
@require_role(['Admin', 'Warehouse'])
def create_product():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'category', 'warranty_years']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'error': f'{field} is required'}), 400

        product = Product(
            name=data['name'],
            category=data['category'],
            warranty_years=data['warranty_years'],
            image_url=data.get('image_url')
        )

        db.session.add(product)
        db.session.commit()

        # Add suppliers if provided
        if 'supplier_ids' in data:
            for supplier_id in data['supplier_ids']:
                supplier = Supplier.query.get(supplier_id)
                if supplier:
                    product.suppliers.append(supplier)
            db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'warranty_years': product.warranty_years,
                'image_url': product.image_url
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@require_role(['Admin', 'Warehouse'])
def update_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # Update fields if provided
        if 'name' in data:
            product.name = data['name']
        if 'category' in data:
            product.category = data['category']
        if 'warranty_years' in data:
            product.warranty_years = data['warranty_years']
        if 'image_url' in data:
            product.image_url = data['image_url']

        # Update suppliers if provided
        if 'supplier_ids' in data:
            # Clear existing suppliers
            product.suppliers.clear()
            # Add new suppliers
            for supplier_id in data['supplier_ids']:
                supplier = Supplier.query.get(supplier_id)
                if supplier:
                    product.suppliers.append(supplier)

        db.session.commit()

        return jsonify({
            'success': True,
            'data': {
                'product_id': product.product_id,
                'name': product.name,
                'category': product.category,
                'warranty_years': product.warranty_years,
                'image_url': product.image_url,
                'suppliers': [{'supplier_id': s.supplier_id, 'supplier_name': s.supplier_name}
                              for s in product.suppliers]
            }
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@require_role(['Admin'])
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)

        # Check if product is used in orders or inventory
        if product.order_items or product.inventory_lots:
            return jsonify({
                'success': False,
                'error': 'Cannot delete product that has order items or inventory records'
            }), 400

        db.session.delete(product)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

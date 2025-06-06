from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Role

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')

    if not account or not password:
        return jsonify({'success': False, 'error': 'Account and password are required'}), 400

    # For demo purposes, create hardcoded users if they don't exist
    user = User.query.filter_by(account=account).first()

    if not user:
        # Create demo users
        create_demo_users()
        user = User.query.filter_by(account=account).first()

    if user and check_password_hash(user.pwd_hash, password):
        # Store user info in session
        session['user_id'] = user.user_id
        session['account'] = user.account
        session['role_id'] = user.role_id
        session['role_name'] = user.primary_role.role_name

        return jsonify({
            'success': True,
            'data': {
                'user_id': user.user_id,
                'account': user.account,
                'role_id': user.role_id,
                'role_name': user.primary_role.role_name
            }
        })
    else:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@auth_bp.route('/current-user', methods=['GET'])
def current_user():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401

    user = User.query.get(session['user_id'])
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    return jsonify({
        'success': True,
        'data': {
            'user_id': user.user_id,
            'account': user.account,
            'role_id': user.role_id,
            'role_name': user.primary_role.role_name
        }
    })


def create_demo_users():
    """Create demo users if they don't exist"""
    try:
        # Create roles if they don't exist
        roles_data = [
            {'role_name': 'Admin'},
            {'role_name': 'Sales'},
            {'role_name': 'Warehouse'}
        ]

        for role_data in roles_data:
            role = Role.query.filter_by(
                role_name=role_data['role_name']).first()
            if not role:
                role = Role(**role_data)
                db.session.add(role)

        db.session.commit()

        # Create demo users
        users_data = [
            {'account': 'admin', 'password': 'admin', 'role_name': 'Admin'},
            {'account': 'sales', 'password': 'sales', 'role_name': 'Sales'},
            {'account': 'warehouse', 'password': 'warehouse', 'role_name': 'Warehouse'}
        ]

        for user_data in users_data:
            user = User.query.filter_by(account=user_data['account']).first()
            if not user:
                role = Role.query.filter_by(
                    role_name=user_data['role_name']).first()
                user = User(
                    account=user_data['account'],
                    pwd_hash=generate_password_hash(user_data['password']),
                    role_id=role.role_id
                )
                db.session.add(user)

        db.session.commit()
        print("Demo users created successfully")

    except Exception as e:
        db.session.rollback()
        print(f"Error creating demo users: {e}")


def require_auth(f):
    """Decorator to require authentication"""
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_role(allowed_roles):
    """Decorator to require specific roles"""
    from functools import wraps

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401

            if session.get('role_name') not in allowed_roles:
                return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403

            return f(*args, **kwargs)
        return decorated_function
    return decorator

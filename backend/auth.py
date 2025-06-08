from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import datetime
import os
from models import db, User, Role

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# JWT secret key - in production, use environment variable
JWT_SECRET_KEY = os.getenv(
    'JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_DELTA = datetime.timedelta(hours=24)


def generate_jwt_token(user):
    """Generate JWT token for user"""
    payload = {
        'user_id': user.user_id,
        'account': user.account,
        'role_id': user.role_id,
        'role_name': user.primary_role.role_name,
        'exp': datetime.datetime.utcnow() + JWT_EXPIRATION_DELTA,
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt_token(token):
    """Decode and validate JWT token"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


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
        # Generate JWT token
        token = generate_jwt_token(user)

        return jsonify({
            'success': True,
            'token': token,
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
    # With JWT, logout is handled client-side by removing the token
    return jsonify({'success': True, 'message': 'Logged out successfully'})


@auth_bp.route('/current-user', methods=['GET'])
def current_user():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'success': False, 'error': 'No token provided'}), 401

    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)

    if not payload:
        return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

    user = User.query.get(payload['user_id'])
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
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'success': False, 'error': 'Authentication required'}), 401

        token = auth_header.split(' ')[1]
        payload = decode_jwt_token(token)

        if not payload:
            return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

        # Add user info to request context
        request.current_user = payload
        return f(*args, **kwargs)
    return decorated_function


def require_role(allowed_roles):
    """Decorator to require specific roles"""
    from functools import wraps

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return jsonify({'success': False, 'error': 'Authentication required'}), 401

            token = auth_header.split(' ')[1]
            payload = decode_jwt_token(token)

            if not payload:
                return jsonify({'success': False, 'error': 'Invalid or expired token'}), 401

            if payload.get('role_name') not in allowed_roles:
                return jsonify({'success': False, 'error': 'Insufficient permissions'}), 403

            # Add user info to request context
            request.current_user = payload
            return f(*args, **kwargs)
        return decorated_function
    return decorator

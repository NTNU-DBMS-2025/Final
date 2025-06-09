from flask import Blueprint, request, jsonify
from models import db, User, Role, user_role
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from auth import decode_jwt_token

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


def get_current_user():
    """Get current user from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None

    token = auth_header.split(' ')[1]
    payload = decode_jwt_token(token)

    if not payload:
        return None

    user = User.query.get(payload['user_id'])
    return user


@users_bp.route('', methods=['GET'])
def get_users():
    """Get all users with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        role_filter = request.args.get('role_id', type=int)
        search = request.args.get('search', '').strip()

        # Build query
        query = User.query.join(Role, User.role_id == Role.role_id)

        # Apply filters
        if role_filter:
            query = query.filter(User.role_id == role_filter)
        if search:
            query = query.filter(User.account.contains(search))

        # Order by account name
        query = query.order_by(User.account.asc())

        # Paginate
        pagination = query.paginate(
            page=page, per_page=per_page, error_out=False
        )

        users = []
        for user in pagination.items:
            # Get all roles for this user
            user_roles = [role.role_name for role in user.roles]

            users.append({
                'user_id': user.user_id,
                'account': user.account,
                'role_id': user.role_id,
                'primary_role': user.primary_role.role_name,
                'all_roles': user_roles,
                'created_at': user.user_id  # placeholder for creation date if added to model
            })

        return jsonify({
            'success': True,
            'data': users,
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
            'error': f'Failed to fetch users: {str(e)}'
        }), 500


@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    try:
        user = User.query.get_or_404(user_id)

        # Get all roles for this user
        user_roles = []
        for role in user.roles:
            user_roles.append({
                'role_id': role.role_id,
                'role_name': role.role_name
            })

        return jsonify({
            'success': True,
            'data': {
                'user_id': user.user_id,
                'account': user.account,
                'role_id': user.role_id,
                'primary_role': {
                    'role_id': user.primary_role.role_id,
                    'role_name': user.primary_role.role_name
                },
                'all_roles': user_roles
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch user: {str(e)}'
        }), 500


@users_bp.route('', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['account', 'password', 'role_id']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Validate role exists
        role = Role.query.get(data['role_id'])
        if not role:
            return jsonify({
                'success': False,
                'error': 'Role not found'
            }), 404

        # Check if trying to create Owner role - only Owner can create Owner accounts
        if role.role_name == 'Owner':
            current_user = get_current_user()
            if not current_user:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401

            current_user_primary_role = Role.query.get(current_user.role_id)
            if not current_user_primary_role or current_user_primary_role.role_name != 'Owner':
                return jsonify({
                    'success': False,
                    'error': 'Only Owner can create Owner accounts'
                }), 403

        # Check if trying to create Admin role - only Owner can create Admin accounts
        if role.role_name == 'Admin':
            current_user = get_current_user()
            if not current_user:
                return jsonify({
                    'success': False,
                    'error': 'Authentication required'
                }), 401

            current_user_primary_role = Role.query.get(current_user.role_id)
            if current_user_primary_role and current_user_primary_role.role_name == 'Admin':
                return jsonify({
                    'success': False,
                    'error': 'Admin cannot create other Admin accounts'
                }), 403

        # Check if account already exists
        existing_user = User.query.filter(
            User.account == data['account']).first()
        if existing_user:
            return jsonify({
                'success': False,
                'error': 'Account already exists'
            }), 400

        # Validate password strength
        password = data['password']
        if len(password) < 6:
            return jsonify({
                'success': False,
                'error': 'Password must be at least 6 characters long'
            }), 400

        # Create user
        user = User(
            account=data['account'].strip(),
            pwd_hash=generate_password_hash(password),
            role_id=data['role_id']
        )

        db.session.add(user)
        db.session.flush()  # Get user_id

        # Add user to the primary role in many-to-many table
        user.roles.append(role)

        # Add additional roles if provided
        if 'additional_roles' in data and data['additional_roles']:
            for role_id in data['additional_roles']:
                additional_role = Role.query.get(role_id)
                if additional_role and additional_role not in user.roles:
                    user.roles.append(additional_role)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'data': {
                'user_id': user.user_id,
                'account': user.account,
                'primary_role': role.role_name
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
            'error': f'Failed to create user: {str(e)}'
        }), 500


@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        # Get current user from token
        current_user = get_current_user()
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401

        user = User.query.get_or_404(user_id)
        data = request.get_json()

        # Check if trying to modify an Owner user
        user_primary_role = Role.query.get(user.role_id)
        current_user_primary_role = Role.query.get(current_user.role_id)

        # Only Owner can modify Owner accounts
        if user_primary_role and user_primary_role.role_name == 'Owner':
            if not current_user_primary_role or current_user_primary_role.role_name != 'Owner':
                return jsonify({
                    'success': False,
                    'error': 'Only Owner can modify Owner accounts'
                }), 403

        # Admin cannot modify other Admin accounts
        if user_primary_role and user_primary_role.role_name == 'Admin':
            if current_user_primary_role and current_user_primary_role.role_name == 'Admin' and user.user_id != current_user.user_id:
                return jsonify({
                    'success': False,
                    'error': 'Admin cannot modify other Admin accounts'
                }), 403

        # Account name cannot be modified - removed for security

        # Update password
        if 'password' in data and data['password']:
            password = data['password']
            if len(password) < 6:
                return jsonify({
                    'success': False,
                    'error': 'Password must be at least 6 characters long'
                }), 400

            user.pwd_hash = generate_password_hash(password)

        # Update primary role
        if 'role_id' in data:
            role = Role.query.get(data['role_id'])
            if not role:
                return jsonify({
                    'success': False,
                    'error': 'Role not found'
                }), 404

            # Check if trying to assign Owner role - only Owner can assign Owner role
            if role.role_name == 'Owner':
                if not current_user_primary_role or current_user_primary_role.role_name != 'Owner':
                    return jsonify({
                        'success': False,
                        'error': 'Only Owner can assign Owner role'
                    }), 403

            # Check if Admin trying to assign Admin role - only Owner can assign Admin role
            if role.role_name == 'Admin':
                if current_user_primary_role and current_user_primary_role.role_name == 'Admin':
                    return jsonify({
                        'success': False,
                        'error': 'Admin cannot assign Admin role'
                    }), 403

            user.role_id = data['role_id']

            # Ensure the new primary role is in the user's roles list
            if role not in user.roles:
                user.roles.append(role)

        # Update additional roles
        if 'roles' in data:
            # Clear current roles
            user.roles.clear()

            # Add new roles
            for role_id in data['roles']:
                role = Role.query.get(role_id)
                if role:
                    user.roles.append(role)

            # Ensure primary role is included
            primary_role = Role.query.get(user.role_id)
            if primary_role and primary_role not in user.roles:
                user.roles.append(primary_role)

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update user: {str(e)}'
        }), 500


@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        # Get current user from token
        current_user = get_current_user()
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401

        user = User.query.get_or_404(user_id)

        # Check if trying to delete an Owner user
        user_primary_role = Role.query.get(user.role_id)
        current_user_primary_role = Role.query.get(current_user.role_id)

        # Only Owner can delete Owner accounts
        if user_primary_role and user_primary_role.role_name == 'Owner':
            if not current_user_primary_role or current_user_primary_role.role_name != 'Owner':
                return jsonify({
                    'success': False,
                    'error': 'Only Owner can delete Owner accounts'
                }), 403

        # Admin cannot delete other Admin accounts
        if user_primary_role and user_primary_role.role_name == 'Admin':
            if current_user_primary_role and current_user_primary_role.role_name == 'Admin' and user.user_id != current_user.user_id:
                return jsonify({
                    'success': False,
                    'error': 'Admin cannot delete other Admin accounts'
                }), 403

        # Check if user has associated orders (prevent deletion if they do)
        if user.orders:
            return jsonify({
                'success': False,
                'error': 'Cannot delete user with associated orders'
            }), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete user: {str(e)}'
        }), 500

# Role management endpoints


@users_bp.route('/roles', methods=['GET'])
def get_roles():
    """Get all roles"""
    try:
        roles = Role.query.order_by(Role.role_name).all()

        role_list = []
        for role in roles:
            # Count users with this role
            user_count = User.query.filter(
                User.role_id == role.role_id).count()

            role_list.append({
                'role_id': role.role_id,
                'role_name': role.role_name,
                'user_count': user_count
            })

        return jsonify({
            'success': True,
            'data': role_list
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch roles: {str(e)}'
        }), 500


@users_bp.route('/roles', methods=['POST'])
def create_role():
    """Create a new role"""
    try:
        data = request.get_json()

        # Validate required fields
        if 'role_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: role_name'
            }), 400

        # Check if role already exists
        existing_role = Role.query.filter(
            Role.role_name == data['role_name']).first()
        if existing_role:
            return jsonify({
                'success': False,
                'error': 'Role already exists'
            }), 400

        # Create role
        role = Role(
            role_name=data['role_name'].strip()
        )

        db.session.add(role)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Role created successfully',
            'data': {
                'role_id': role.role_id,
                'role_name': role.role_name
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
            'error': f'Failed to create role: {str(e)}'
        }), 500


@users_bp.route('/roles/<int:role_id>', methods=['PUT'])
def update_role(role_id):
    """Update an existing role"""
    try:
        role = Role.query.get_or_404(role_id)
        data = request.get_json()

        # Update role name
        if 'role_name' in data:
            # Check if new role name already exists
            existing_role = Role.query.filter(
                Role.role_name == data['role_name'],
                Role.role_id != role_id
            ).first()

            if existing_role:
                return jsonify({
                    'success': False,
                    'error': 'Role name already exists'
                }), 400

            role.role_name = data['role_name'].strip()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Role updated successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to update role: {str(e)}'
        }), 500


@users_bp.route('/roles/<int:role_id>', methods=['DELETE'])
def delete_role(role_id):
    """Delete a role (only if no users are assigned to it)"""
    try:
        role = Role.query.get_or_404(role_id)

        # Check if any users have this as their primary role
        users_with_role = User.query.filter(User.role_id == role_id).count()
        if users_with_role > 0:
            return jsonify({
                'success': False,
                'error': 'Cannot delete role with assigned users'
            }), 400

        db.session.delete(role)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Role deleted successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to delete role: {str(e)}'
        }), 500

# User role assignment endpoints


@users_bp.route('/<int:user_id>/roles', methods=['POST'])
def assign_role_to_user(user_id):
    """Assign a role to a user"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if 'role_id' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: role_id'
            }), 400

        role = Role.query.get(data['role_id'])
        if not role:
            return jsonify({
                'success': False,
                'error': 'Role not found'
            }), 404

        # Check if user already has this role
        if role in user.roles:
            return jsonify({
                'success': False,
                'error': 'User already has this role'
            }), 400

        # Assign role
        user.roles.append(role)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Role assigned to user successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to assign role: {str(e)}'
        }), 500


@users_bp.route('/<int:user_id>/roles/<int:role_id>', methods=['DELETE'])
def remove_role_from_user(user_id, role_id):
    """Remove a role from a user"""
    try:
        user = User.query.get_or_404(user_id)
        role = Role.query.get_or_404(role_id)

        # Cannot remove primary role
        if user.role_id == role_id:
            return jsonify({
                'success': False,
                'error': 'Cannot remove primary role. Change primary role first.'
            }), 400

        # Check if user has this role
        if role not in user.roles:
            return jsonify({
                'success': False,
                'error': 'User does not have this role'
            }), 400

        # Remove role
        user.roles.remove(role)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Role removed from user successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to remove role: {str(e)}'
        }), 500

# Statistics endpoint


@users_bp.route('/stats', methods=['GET'])
def get_user_stats():
    """Get user statistics"""
    try:
        total_users = User.query.count()

        # Users by role
        role_stats = db.session.query(
            Role.role_name,
            func.count(User.user_id).label('user_count')
        ).join(User, Role.role_id == User.role_id)\
         .group_by(Role.role_id, Role.role_name)\
         .order_by(func.count(User.user_id).desc()).all()

        role_breakdown = [
            {
                'role_name': stat[0],
                'user_count': stat[1]
            } for stat in role_stats
        ]

        # Total roles
        total_roles = Role.query.count()

        return jsonify({
            'success': True,
            'data': {
                'total_users': total_users,
                'total_roles': total_roles,
                'role_breakdown': role_breakdown
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch user statistics: {str(e)}'
        }), 500

# Password management endpoints


@users_bp.route('/<int:user_id>/reset-password', methods=['PUT'])
def reset_password(user_id):
    """Reset user password to account name"""
    try:
        # Get current user from token
        current_user = get_current_user()
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401

        user = User.query.get_or_404(user_id)

        # Check authorization for password reset
        user_primary_role = Role.query.get(user.role_id)
        current_user_primary_role = Role.query.get(current_user.role_id)

        # Only Owner can reset Owner accounts
        if user_primary_role and user_primary_role.role_name == 'Owner':
            if not current_user_primary_role or current_user_primary_role.role_name != 'Owner':
                return jsonify({
                    'success': False,
                    'error': 'Only Owner can reset Owner passwords'
                }), 403

        # Admin cannot reset other Admin accounts
        if user_primary_role and user_primary_role.role_name == 'Admin':
            if current_user_primary_role and current_user_primary_role.role_name == 'Admin' and user.user_id != current_user.user_id:
                return jsonify({
                    'success': False,
                    'error': 'Admin cannot reset other Admin passwords'
                }), 403

        # Reset password to account name
        user.pwd_hash = generate_password_hash(user.account)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password reset successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to reset password: {str(e)}'
        }), 500


@users_bp.route('/<int:user_id>/change-password', methods=['PUT'])
def change_password(user_id):
    """Change user password"""
    try:
        # Get current user from token
        current_user = get_current_user()
        if not current_user:
            return jsonify({
                'success': False,
                'error': 'Authentication required'
            }), 401

        # Users can only change their own password
        if current_user.user_id != user_id:
            return jsonify({
                'success': False,
                'error': 'Access denied - can only change your own password'
            }), 403

        user = User.query.get_or_404(user_id)
        data = request.get_json()

        # Validate required fields
        required_fields = ['current_password', 'new_password']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400

        # Verify current password
        if not check_password_hash(user.pwd_hash, data['current_password']):
            return jsonify({
                'success': False,
                'error': 'Current password is incorrect'
            }), 400

        # Validate new password
        new_password = data['new_password']
        if len(new_password) < 6:
            return jsonify({
                'success': False,
                'error': 'New password must be at least 6 characters long'
            }), 400

        # Update password
        user.pwd_hash = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': f'Failed to change password: {str(e)}'
        }), 500

from flask import Blueprint, jsonify, request
from app.models import User
from app.services import UserService
from http import HTTPStatus
from app.serialiers import serialize_user

api_bp = Blueprint('api_bp', __name__)


@api_bp.route('/health-check')
def health_check():
    return jsonify({"message": "Ok"})

# ====================================================================
# User route
# ====================================================================


@api_bp.route('/users', methods=['GET'])
def get_users():
    users = UserService.get_all_users()
    total_users = UserService.get_total_user()
    return jsonify({
        'users': [serialize_user(user) for user in users],
        'total_user': total_users
    }), HTTPStatus.OK


@api_bp.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON payload'}), HTTPStatus.BAD_REQUEST

        name = data.get('name', '').strip()
        if not name:
            return jsonify({'error': 'Name is required and cannot be empty'}), HTTPStatus.BAD_REQUEST

        # Check if user already exists
        is_exist = UserService.get_user_by_name(name)
        if is_exist:
            return jsonify({'error': f'User with name:"{name}" already exists'}), HTTPStatus.CONFLICT

        # Create new user
        user = UserService.create_user(name)
        return jsonify(serialize_user(user)), HTTPStatus.CREATED

    except ValueError as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
    except Exception:
        return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserService.get_user_by_id(user_id)
        if user:
            return jsonify(serialize_user(user)), HTTPStatus.OK
        return jsonify({
            'error': 'User with id:{} not found'.format(user_id)
        }), HTTPStatus.NOT_FOUND
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user name"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Name is required'}), HTTPStatus.BAD_REQUEST

        user = UserService.update_user(user_id, data['name'].strip())
        if not user:
            return jsonify({'error': 'User not found or is deleted'}), HTTPStatus.NOT_FOUND
        return jsonify(serialize_user(user)), HTTPStatus.OK
    except Exception:
        return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def soft_delete_user(user_id):
    user = UserService.soft_delete_user(user_id)
    if not user:
        return jsonify({'error': 'User not found or already deleted'}), HTTPStatus.NOT_FOUND

    return jsonify({'message': f'User {user_id} soft-deleted successfully'}), HTTPStatus.OK


@api_bp.route('/users/<int:user_id>', methods=['PATCH'])
def restore_user(user_id):
    user = UserService.restore_user(user_id)
    if not user:
        return jsonify({'error': f'User id:{user_id} not found or already deleted'})

    return jsonify({'message': f'User id:{user_id} restore successfully'})


@api_bp.route('/users/trash/', methods=['GET'])
@api_bp.route('/users/trash/<int:user_id>', methods=['GET'])
def trask_user(user_id=None):
    """
    Retrieve soft-delete user
    - if `user_id` is provided, return a specific user.
    - if no `user_id`, return all soft-delete user
    """
    try:
        if user_id:
            user = UserService.trask_users(user_id)
            if not user:
                return jsonify({'message': 'User not found in trash'}), HTTPStatus.NOT_FOUND
            return jsonify({'user': serialize_user(user)}), HTTPStatus.OK
        else:
            users = UserService.trask_users()
            if not users:
                return jsonify({'message': 'Not users found in trash'}), HTTPStatus.NOT_FOUND
            return jsonify({'users': [serialize_user(user) for user in users]}), HTTPStatus.OK
    except Exception:
        return jsonify({'error': 'Internal server error'}), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/users/permanent/<int:user_id>', methods=['DELETE'])
def permanent_delete_user(user_id):
    """Permanent delete user"""
    user = UserService.permanent_delete_user(user_id)
    if not user:
        return jsonify({'error': f'User id:{user_id} not found'}), HTTPStatus.NOT_FOUND

    return jsonify({'message': f'User id:{user_id} delete successfully.'})
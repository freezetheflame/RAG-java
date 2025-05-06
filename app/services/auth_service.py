import uuid
import datetime
import jwt
from zoneinfo import ZoneInfo
from app.extensions import db
from app.models.user import User
from flask import jsonify
from app.config import Settings
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    user_type = data.get('user_type', 'normal')

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, password=hashed_password, email=email, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'Registration successful! id': new_user.id}), 201


def login_user(data):
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        payload = {
            'user_id': user.id,
            'user_type': user.user_type,
            'exp': datetime.datetime.now(ZoneInfo('Asia/Shanghai')) + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, Settings.SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401

def get_user_info(jwt_token):
    try:
        payload = jwt.decode(jwt_token, Settings.SECRET_KEY, algorithms='HS256')
        user_id = payload.get('user_id')
        user_type = payload.get('user_type')
        user = User.query.get(user_id)
        if user:
            return jsonify({'user_id': user.id, 'user_type': user_type, 'email': user.email,'user_name': user.username, 'create_time': user.created_at}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Expired token'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401

    return jsonify({'error': 'User not found'}), 404

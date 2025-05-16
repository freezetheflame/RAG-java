from flask import request, g, jsonify
import jwt
from functools import wraps
from app.config import Settings
from app.models.user import User

def token_required(f):
    @wraps(f)
    async def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            payload = jwt.decode(token, Settings.SECRET_KEY, algorithms='HS256')
            user_id = payload.get('user_id')
            user = User.query.get(user_id)
            g.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        return await f(*args, **kwargs)
    return decorated

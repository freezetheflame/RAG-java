from flask import  Blueprint,  request

from app.services.auth_service import register_user, login_user, get_user_info

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
async def register():
    data = request.get_json()
    return register_user(data)

@bp.route('/login', methods=['POST'])
async def login():
    data = request.get_json()
    return login_user(data)

@bp.route('/info', methods=['GET'])
async def user_info():
    data = request.headers.get('Authorization')
    return get_user_info(data)
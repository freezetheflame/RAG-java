from flask import Blueprint, request,jsonify, g

from app.utils.tokenUtils import token_required
from app.services.file_service import store_file

bp = Blueprint('knowledge_base', __name__, url_prefix='/knowledge_base')

@bp.route('/upload_file', methods=['POST'])
@token_required
async def upload_file():
    user = g.usert
    if user.user_type != 'Administrator':
        return jsonify({'error': 'You are not authorized'}), 401

    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    files = request.files.getlist('files')
    return store_file(files)







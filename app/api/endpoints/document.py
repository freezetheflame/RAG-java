from flask import jsonify, Blueprint

from app.db.doc_to_oss import DocToOSS

bp = Blueprint('document', __name__)


'''
method: GET
content: return the file by name from oss
'''
@bp.route('/document/{name}',methods=['GET'])
async def get_document(name):
    ossService = DocToOSS()
    try:
        file_url = ossService.get_file(name)
        return jsonify({"file_url": file_url}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

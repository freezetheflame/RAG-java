from urllib.parse import quote

from flask import jsonify, Blueprint
from flask import Response

from app.db.doc_to_oss import DocToOSS

bp = Blueprint('document', __name__)


'''
method: GET
content: return the file by name from oss
'''
@bp.route('/document/<name>',methods=['GET'])
async def get_document(name):
    ossService = DocToOSS()
    try:
        file_url = ossService.get_file(name)

        response = Response(
            file_url,
            status=200,
            content_type='application/pdf',
            headers={'Content-Disposition': f"inline; filename*=UTF-8''{quote(name)}"}
        )
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

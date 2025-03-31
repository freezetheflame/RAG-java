'''
basic chat endpoint
'''

from flask import request, jsonify, Blueprint

from app.api.dependency import get_llm_service_dependency

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['POST'])
async def chat():
    provider = request.args.get('provider', 'deepseek')
    prompt = request.json['prompt']

    service = get_llm_service_dependency(provider)

    result = await service.agenerate(prompt)

    return jsonify({'result': result,
                    'provider': provider})


from flask import Blueprint, request, jsonify

from app.services.rag import RAGService

bp = Blueprint('search', __name__)

@bp.route('/search', methods=['POST'])
async def search():
    try:
        # 1. 解析请求数据
        data = request.get_json()
        query = data.get("query")
        top_k = data.get("top_k", 5)  # 默认检索前 5 条结果

        if not query:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        # 2. 初始化 RAG 服务
        rag_service = RAGService(LLMrequire='deepseek')

        # 3. 执行 RAG 查询
        result = await rag_service.query(query, top_k=top_k)

        # 4. 构造响应
        return jsonify({
            "answer": result["answer"],
            "retrieved_docs": result["retrieved_docs"]
        })

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"error": str(e)}), 500

@bp.route('hybrid_search', methods=['POST'])
async def hybrid_search():
    try:
        # 1. 解析请求数据
        data = request.get_json()
        query = data.get("query")
        top_k = data.get("top_k", 5)  # 默认检索前 5 条结果

        if not query:
            return jsonify({"error": "Missing 'query' in request body"}), 400

        # 2. 初始化 RAG 服务
        rag_service = RAGService(LLMrequire='deepseek')

        # 3. 执行 RAG 查询
        result = await rag_service.query(query, top_k=top_k)

        # 4. 构造响应
        return jsonify({
            "answer": result["answer"],
            "retrieved_docs": result["retrieved_docs"]
        })

    except Exception as e:
        # 捕获异常并返回错误信息
        return jsonify({"error": str(e)}), 500
import os

from flask import Blueprint, request, current_app

from app.utils.tokenUtils import token_required
from flask import jsonify, g

uploadbp = Blueprint('upload', __name__, url_prefix='/upload')

# 本文件用于用户自定义文件上传以及管理员查看所有oss上的文件
@uploadbp.route('/file', methods=['POST'])
@token_required
def upload_new_file():
    user = g.usert
    if user.user_type != 'Administrator':
        return jsonify({'error': 'You are not authorized'}), 401

    file = request.files.get('file')
    if not file:
        return {"error": "No file provided"}, 400
        # 检查文件类型
    if not file.filename.endswith(('.pdf', '.md')):
        return {"error": "Unsupported file type"}, 400
    # 保存文件到指定目录
    # 构建目标路径（推荐使用绝对路径）
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 当前文件所在目录
    upload_folder = os.path.join(base_dir, 'data')

    # 如果 data 目录不存在，自动创建
    os.makedirs(upload_folder, exist_ok=True)

    # 构建完整文件路径
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    # 处理文件
    pipeline = current_app.extensions['pipeline']
    pipeline.process_document(file_path)
    # 上传到OSS
    ossloader = current_app.extensions['oss']
    ossloader.upload_file(file_path)
    # 删除本地文件
    os.remove(file_path)
    # 返回处理结果
    return {"message": "File uploaded and processed successfully"}, 200


@uploadbp.route('/files', methods=['GET'])
def list_files():
    """
    列出所有上传的文件
    """
    # 获取文件列表
    ossloader = current_app.extensions['oss']
    files = ossloader.list_files()
    # 返回文件列表
    return {"files": files}, 200

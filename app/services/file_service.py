from werkzeug.utils import secure_filename
from flask import jsonify
import os
from app.db.doc_to_oss import DocToOSS
from app.pipelines.pipeline import ProcessingPipeline


MAX_FILE_SIZE = 20 * 1024 * 1024 # 单个文件最大20MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'} # 允许的文件类型
doc_to_oss = DocToOSS()
processed_pipeline = ProcessingPipeline()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def store_file(files):
    saved_files = []
    for file in files:
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file'}), 400

        # 验证文件大小
        file.seek(0, os.SEEK_END)
        file_siem = file.tell()
        file.seek(0)
        if file_siem > MAX_FILE_SIZE:
            return jsonify({'error': 'File too big'}), 400

        file_name = secure_filename(file.filename)
        error = doc_to_oss.upload_file_to_oss(file.stream, file_name)
        if error:
            return jsonify({'error': error}), 400

        saved_files.append(file_name)
        # 处理文件
        processed_pipeline.process_document(file.stream, file_name)

    return jsonify({'success': True, 'saved_files': saved_files}), 200
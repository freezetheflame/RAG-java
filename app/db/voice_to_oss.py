import os
import uuid
from datetime import datetime

from oss2 import Bucket, Auth

from app.config import Settings
import oss2


OSS_END_POINT = 'oss-cn-beijing.aliyuncs.com'

class Voice_to_oss:
    def __init__(self, bucket_name: str = 'javarag'):
        self.ACCESS_KEY_ID = Settings.Aliyun_AK_ID
        self.ACCESS_KEY_SECRET = Settings.Aliyun_AK_SECRET
        self.auth = Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET)
        self.ENDPOINT_URL = OSS_END_POINT
        self.bucket_name = bucket_name
        self.base_url = f'https://{self.bucket_name}.{OSS_END_POINT}/'
        self.bucket = Bucket(self.auth, self.ENDPOINT_URL, self.bucket_name)

    def generate_temp_url(self, object_key, expires=3600):
        """生成临时访问URL"""
        return self.bucket.sign_url('GET', object_key, expires)

    def upload_file(self, file_path, prefix='audio/'):
        """
        上传文件到OSS并返回临时URL
        :param file_path: 本地文件路径
        :param prefix: OSS存储路径前缀
        :return: (object_key, temp_url)
        """
        # 生成唯一文件名
        ext = os.path.splitext(file_path)[1]
        object_key = prefix + datetime.now().strftime('%Y%m%d') + '/' + str(uuid.uuid4()) + ext

        # 上传文件
        self.bucket.put_object_from_file(object_key, file_path)

        # 生成临时URL（1小时有效）
        temp_url = self.generate_temp_url(object_key)
        return object_key, temp_url

    def cleanup_file(self, object_key):
        """清理OSS文件"""
        self.bucket.delete_object(object_key)

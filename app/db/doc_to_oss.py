import os

import oss2
from app.config import Settings
from urllib.parse import quote


class DocToOSS:
    def __init__(self, bucket_name : str = 'rag-java'):
        self.ACCESS_KEY_ID = Settings.ACCESS_KEY_ID
        self.ACCESS_KEY_SECRET = Settings.ACCESS_KEY_SECRET
        self.ENDPOINT_URL = Settings.ENDPOINT_URL
        self.bucket_name = bucket_name


    def get_file(self, file_name):
            auth = oss2.Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET)
            bucket = oss2.Bucket(auth, self.ENDPOINT_URL, self.bucket_name)

            # 设置过期时间
            expiry_seconds = 3600

            url = bucket.sign_url('GET', file_name, expiry_seconds)
            return url

    def upload_file(self,file_path):
        auth = oss2.Auth(self.ACCESS_KEY_ID, self.ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, self.ENDPOINT_URL, self.bucket_name)
        bucket.put_object_from_file(os.path.basename(file_path), file_path)
        print(f"文件 {file_path} 上传成功")


if __name__ == '__main__':
    doc_to_oss = DocToOSS()
    url = doc_to_oss.get_file('ComputerArchitecture.pdf')
    print(url)
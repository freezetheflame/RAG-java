import os
import re
from bs4 import BeautifulSoup
from markdownify import markdownify
from urllib.parse import urljoin
import requests
from datetime import datetime


class BaseCrawler:
    def __init__(self, base_url, output_dir="data/raw"):
        self.base_url = base_url
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def sanitize_filename(self, title):
        """生成安全的文件名"""
        name = re.sub(r'[^\w\-_\. ]', '_', title)[:150]
        return f"{datetime.now().strftime('%Y%m%d')}_{name}.md"

    def fetch_to_markdown(self, url, selector="main"):
        """获取网页并转换为Markdown"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.select_one(selector) or soup.body

            # 转换相对链接为绝对链接
            for a in content.find_all('a', href=True):
                a['href'] = urljoin(url, a['href'])

            return markdownify(str(content))
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def save_content(self, title, content):
        """保存Markdown文件"""
        if not content:
            return False

        filename = os.path.join(self.output_dir, self.sanitize_filename(title))
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"Source: {self.base_url}\n\n")
            f.write(content)
        return True
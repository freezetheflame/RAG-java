from urllib.parse import urlparse, urljoin

from .base_crawler import BaseCrawler

class JavaOfficialCrawler(BaseCrawler):
    def crawl_jdk_docs(self, version=17):
        """爬取Oracle JDK官方文档"""
        url = f"https://docs.oracle.com/en/java/javase/{version}/docs/api/index.html"
        content = self.fetch_to_markdown(url, selector="div.contentContainer")
        self.save_content(f"Java_{version}_API_Documentation", content)

class SpringCrawler(BaseCrawler):
    def crawl_spring_docs(self, module="spring-framework"):
        """爬取Spring官方文档"""
        url = f"https://docs.spring.io/{module}/docs/current/reference/html/"
        content = self.fetch_to_markdown(url, selector="div.book")
        self.save_content(f"Spring_{module}_Docs", content)


class NowcoderCrawler(BaseCrawler):
    def crawl(self, keyword="Java面试", max_pages=3):
        """增强的爬取逻辑，支持子链接抓取"""
        initial_url = urljoin(self.base_url, f"/search?query={keyword}")
        visited = set()
        queue = [initial_url]
        pages_crawled = 0

        while queue and pages_crawled < max_pages:
            current_url = queue.pop(0)

            if current_url in visited:
                continue
            visited.add(current_url)

            print(f"Crawling: {current_url}")
            title, content, links = self.fetch_to_markdown(current_url, "div.search-result")

            if not content:
                continue

            # 保存内容并计数
            if self.save_content(title, content, current_url):
                pages_crawled += 1
                print(f"Successfully saved: {title}")

            # 处理子链接
            parsed_base = urlparse(self.base_url)
            for link in links:
                # 过滤非本站链接和已访问链接
                parsed_link = urlparse(link)
                if parsed_link.netloc == parsed_base.netloc and link not in visited:
                    if link not in queue:
                        queue.append(link)

        print(f"Crawling completed. Total pages crawled: {pages_crawled}")
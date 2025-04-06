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
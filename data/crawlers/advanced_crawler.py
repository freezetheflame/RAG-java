# crawlers/advanced_crawler.py
from markdownify import markdownify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class AdvancedCrawler:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self._setup_options()
        self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 20)

    def _setup_options(self):
        """反爬配置"""
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0")

        # 关键反检测配置
        self.options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        self.options.add_experimental_option("useAutomationExtension", False)

        # 使用新版无头模式
        self.options.add_argument("--headless=new")

        # 初始化driver
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                    window.navigator.chrome = undefined
                """
        })

    def crawl_juejin(self, keyword="Java面试", max_pages=3):
        try:
            self.driver.get(f"https://juejin.cn/search?query={keyword}")

            # 混合等待策略
            time.sleep(3)  # 必须的初始等待
            self.wait.until(
                lambda d: d.execute_script(
                    'return document.readyState === "complete" && '
                    'document.body.innerText.includes("推荐")'
                )
            )

            # 使用更宽松的定位方式
            items = self.driver.find_elements(
                By.XPATH, "//*[contains(@class,'content') or contains(@class,'article')]//a[contains(@href,'/post/')]"
            )

            return [
                {
                    "title": item.text,
                    "link": item.get_attribute("href"),
                    "source": "掘金"
                } for item in items[:5]  # 限制数量避免触发反爬
            ]
        finally:
            self.driver.quit()

    def get_article_detail(self, url):
        """获取文章详情（含反爬绕过）"""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))

        # 模拟人类阅读行为
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(0.5)

        # 提取内容
        content = self.driver.find_element(By.TAG_NAME, "article").get_attribute("innerHTML")
        return self._clean_content(content)

    def _clean_content(self, html):
        """清洗掘金文章内容"""
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # 移除广告和无关元素
        for tag in soup.select(".marketing-box, .recommend-box"):
            tag.decompose()

        # 转换代码块
        for pre in soup.select("pre"):
            code = pre.select_one("code")
            if code:
                pre.replace_with(f"\n```java\n{code.text}\n```\n")

        return markdownify(str(soup))

    def close(self):
        self.driver.quit()
from crawlers.advanced_crawler import AdvancedCrawler
from processors.interview_parser import InterviewParser

# 初始化
crawler = AdvancedCrawler()
parser = InterviewParser()
print("开始抓取掘金数据...")
# 抓取掘金前3页
articles = crawler.crawl_juejin(max_pages=3)
print(f"抓取到 {len(articles)} 篇文章")
# 抓取详情并解析
structured_data = []
for article in articles[:5]:  # 示例抓取前5篇
    detail = crawler.get_article_detail(article["link"])
    parsed = parser.parse_content(detail)
    structured_data.append({
        "source": "掘金",
        "title": article["title"],
        **parsed
    })
    print(f"抓取标题: {article['title']}")

crawler.close()

import json
from pathlib import Path

output_dir = Path("data/interviews")
output_dir.mkdir(exist_ok=True)

with open(output_dir / "juejin_interviews.json", "w", encoding="utf-8") as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=2)
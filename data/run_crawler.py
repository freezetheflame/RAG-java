from crawlers.java_crawler import JavaOfficialCrawler, SpringCrawler

if __name__ == "__main__":
    # JDK文档采集
    jdk_crawler = JavaOfficialCrawler("https://docs.oracle.com/javase")
    jdk_crawler.crawl_jdk_docs(version=17)

    # Spring文档采集
    spring_crawler = SpringCrawler("https://docs.spring.io")
    spring_crawler.crawl_spring_docs(module="spring-framework")

    print("爬取任务完成！结果保存在 data/raw 目录")
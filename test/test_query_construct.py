from app.core.query.construct import QueryPipeline

if __name__ == "__main__":
    pipeline = QueryPipeline()
    result = pipeline.process("如何用Python分析气候变化数据？", lang="zh")
    print(result)
from app.core.query.construct import RAGPipeline

if __name__ == "__main__":
    pipeline = RAGPipeline()
    result = pipeline.process("如何用Python分析气候变化数据？", lang="zh")
    print(result)
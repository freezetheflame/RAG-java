import asyncio
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from langchain_community.chat_models import ChatOpenAI

from app.config import Settings
from data.build.Embedding import VectorDB, EmbeddingGenerator
from data.build.chunk import AdvancedChunker
from data.build.tokenizer import ChineseTokenizer


class ProcessingPipeline:
    def __init__(self):
        self.chunker = AdvancedChunker()
        self.tokenizer = ChineseTokenizer()
        self.VectorDB = VectorDB(milvus_uri=Settings.MILVUS_URL,token=Settings.MILVUS_TOKEN,collection_name="advanced_java_docs")
        self.embedding = EmbeddingGenerator(model_name='BAAI/bge-small-zh-v1.5')
        self.llm = ChatOpenAI(model_name = "hunyuan-lite",api_key = Settings.HUNYUAN_API_KEY,base_url="https://api.hunyuan.cloud.tencent.com/v1")

    def process_file_path(self,file_path:str)->str:
        #extract name out of path
        file_name = os.path.basename(file_path)
        return file_name


    def process_document(self, file_path):
        """完整处理流水线"""
        # 分块处理
        if file_path.endswith(".pdf"):
            chunks = self.chunker.process_pdf(file_path)
        else:
            chunks = self.chunker.process_markdown(file_path)
        print("-------------chunking ready-------------")
        # 并行分词
        tokenized_chunks = [self._process_chunk(chunk) for chunk in chunks]
        print("--------------token and embedding ready---------------")
        #添加chunk元数据
        for idx, chunk in enumerate(tokenized_chunks):
            chunk.update({
                "file_name": self.process_file_path(file_path),
                "chunk_index": idx,
                # "token_count": len(chunk["tokens"])
            })

        self.VectorDB.add_documents(tokenized_chunks)
        print("--------------vectorized done--------------")
        return tokenized_chunks

    def _process_chunk(self, chunk):
        """单个分块处理"""
        # 首先调用ai服务生成summary
        message = [
            {"role": "user", "content": f"请为以下内容生成一个简短的总结：\n\n{chunk}"}
        ]
        summary = self.llm.invoke(message)
        summary_str = summary.content
        print(f"summary: {summary}")
        return {
            "raw_text": chunk,
            # "tokens": self.tokenizer.tokenize(chunk),
            "chunk_vector": self.embedding.generate(chunk),
            "summary": summary_str,
            "summary_vector": self.embedding.generate(summary_str),
            "keywords": self.tokenizer.extract_keywords(chunk)
        }


import os

from app.config import Settings
from app.pipelines.Embedding import VectorDB, EmbeddingGenerator
from app.pipelines.chunk import AdvancedChunker
from app.pipelines.tokenizer import ChineseTokenizer


class ProcessingPipeline:
    def __init__(self):
        self.chunker = AdvancedChunker()
        self.tokenizer = ChineseTokenizer()
        self.VectorDB = VectorDB(milvus_uri=Settings.MILVUS_URL,token=Settings.MILVUS_TOKEN)
        self.embedding = EmbeddingGenerator(model_name='BAAI/bge-small-zh-v1.5')


    def process_file_path(self,file_path:str)->str:
        #extract name out of path
        file_name = os.path.basename(file_path)
        return file_name


    def process_document(self, file_stream, file_name):
        """完整处理流水线"""
        # 分块处理
        if file_name.endswith(".pdf"):
            chunks = self.chunker.process_pdf(file_stream)
        else:
            chunks = self.chunker.process_markdown(file_stream)
        print("-------------chunking ready-------------")
        # 并行分词
        tokenized_chunks = [self._process_chunk(chunk) for chunk in chunks]
        print("--------------token and embedding ready---------------")
        #添加chunk元数据
        for idx, chunk in enumerate(tokenized_chunks):
            chunk.update({
                "file_name": file_name,
                "chunk_index": idx,
            })

        self.VectorDB.add_documents(tokenized_chunks)
        print("--------------vectorized done--------------")
        return tokenized_chunks

    def _process_chunk(self, chunk):
        """单个分块处理"""
        return {
            "raw_text": chunk,
            # "tokens": self.tokenizer.tokenize(chunk),
            "vector": self.embedding.generate(chunk),
            "keywords": self.tokenizer.extract_keywords(chunk)
        }
import os

from unstructured.partition.pdf import partition_pdf
from unstructured.partition.md import partition_md
from langchain.text_splitter import RecursiveCharacterTextSplitter


class AdvancedChunker(RecursiveCharacterTextSplitter):
    def __init__(self):
        self.min_chunk_size = 300
        # 初始化分块器（针对中文优化）
        super().__init__(
            chunk_size=1000,
            chunk_overlap=80,
            separators= self.get_dynamic_separators(),
            length_function=len,
            # ["\n## ", "\n### ", "\n\n", "\n", "。", "！", "？", "……"]
        )

    def get_dynamic_separators(self, text=None):
        """根据文本特征返回分隔符优先级"""
        base_separators = ["\n## ", "\n### ", "\n\n", "\n", "。", "！", "？"]
        if text and "```" in text:
            return ["```"] + base_separators  # 代码块优先
        return base_separators

    def split_text(self, text):
        # no预处理：合并过短段落
        text = self._preprocess_text(text)
        chunks = super().split_text(text)
        return chunks


    def _preprocess_text(self, text):
        """合并短段落"""
        lines = text.split('\n')
        merged = []
        buffer = ""

        for line in lines:
            if len(buffer + line) < self.min_chunk_size:
                buffer += line + "\n"
            else:
                merged.append(buffer)
                buffer = line + "\n"
        if buffer:
            merged.append(buffer)
        return "\n".join(merged)

    def _postprocess_chunks(self, chunks):
        """合并过小分块"""
        processed = []
        temp_chunk = ""

        for chunk in chunks:
            if len(temp_chunk + chunk) < self.min_chunk_size:
                temp_chunk += chunk
            else:
                if temp_chunk:
                    processed.append(temp_chunk)
                temp_chunk = chunk
        if temp_chunk:
            processed.append(temp_chunk)

        return processed



    def process_pdf(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"文件 {file_path} 不存在")
        # 使用Unstructured提取PDF元素（文本+表格+图片描述）
        print(f"开始处理PDF文件: {file_path}")
        elements = partition_pdf(
            filename=file_path,
            strategy="fast",  # fast
            extract_images_in_pdf=False,
            infer_table_structure=True,
            include_page_breaks=True,
        )

        if(elements.__len__() == 0):
            raise ValueError("PDF内容为空，请检查PDF文件")

        # 提取纯文本内容
        text_content = "\n".join([e.text for e in elements if hasattr(e, 'text')])
        if(text_content.__len__() == 0):
            raise ValueError("PDF内容为空，请检查PDF文件")
        # 分块处理
        chunks = self.split_text(text_content)
        if(chunks.__len__() == 0):
            raise ValueError("分块失败，请检查PDF内容")
        return chunks

    # chunk.py 更新后的 process_markdown 方法
    def process_markdown(self, file_path):
        """兼容新版unstructured的Markdown处理方法"""
        try:
            elements = partition_md(filename=file_path)

            structured_text = []
            for elem in elements:
                # 新版unstructured兼容写法
                elem_type = getattr(elem, "type", elem.__class__.__name__)

                if elem_type in ["Header", "Title", "NarrativeText"]:
                    structured_text.append(f"# {elem.text}" if elem_type in ["Header", "Title"] else elem.text)
                elif elem_type == "Code":
                    structured_text.append(f"```\n{elem.text}\n```")

            return self.split_text("\n".join(structured_text))

        except ImportError:
            # 回退方案：直接读取原始文本
            with open(file_path, "r", encoding="utf-8") as f:
                return self.split_text("\n".join(f.read()))

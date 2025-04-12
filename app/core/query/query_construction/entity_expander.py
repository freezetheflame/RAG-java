import os
from .base import QueryConstructor
import jieba.posseg as pseg  # 使用 jieba 的词性标注功能
from typing import List, Dict


class EntityExpander(QueryConstructor):
    def __init__(self, synonym_mapping: Dict[str, List[str]] = None):
        """
        :param synonym_mapping: 自定义实体同义词映射，格式示例: {"AI芯片": ["GPU", "TPU", "神经网络处理器"]}
        """
        # 获取当前脚本的目录
        script_dir = os.path.dirname(__file__)
        # 构建文件路径
        file_path = os.path.join(script_dir, "java_synonyms.txt")
        self.synonym_mapping = synonym_mapping or load_synonyms(file_path)

    def build(self, query: str) -> dict:
        # 使用 jieba 进行分词和词性标注
        words = pseg.cut(query)

        entities = []
        expanded_terms = []

        # 1. 实体识别（提取名词和专有名词）
        for word, flag in words:
            if flag.startswith("n"):  # 名词（包括普通名词和专有名词）
                entities.append({
                    "text": word,
                    "label": flag,  # 词性标签
                    "start": query.find(word),  # 起始位置
                    "end": query.find(word) + len(word)  # 结束位置
                })

        # 2. 实体扩展（添加同义词）
        for ent in entities:
            expanded = self.synonym_mapping.get(ent["text"], [])
            expanded_terms.extend([ent["text"]] + expanded)  # 保留原词+扩展词

        # 3. 生成增强后的查询
        enhanced_query = {
            "original_query": query,
            "entities": entities,
            "expanded_terms": list(set(expanded_terms)),  # 去重
            "augmented_query": f"{query} {' '.join(expanded_terms)}"
        }

        return enhanced_query


def load_synonyms(file_path):
    """
    从指定的文件路径加载同义词字典。

    :param file_path: 同义词字典文件的路径
    :return: 一个字典，键是主词，值是同义词列表
    """
    synonym_mapping = {}

    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
    else:
        print(f"加载同义词文件: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    synonyms = [synonym.strip() for synonym in parts[1].split(',')]
                    synonym_mapping[key] = synonyms

    return synonym_mapping
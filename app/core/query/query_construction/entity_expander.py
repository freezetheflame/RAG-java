from .base import QueryConstructor
import spacy
from typing import List, Dict


class EntityExpander(QueryConstructor):
    def __init__(self, model_name="zh_core_web_sm", synonym_mapping: Dict[str, List[str]] = None):
        """
        :param model_name: spaCy预训练模型名称（中文推荐zh_core_web_sm，英文推荐en_core_web_sm）
        :param synonym_mapping: 自定义实体同义词映射，格式示例: {"AI芯片": ["GPU", "TPU", "神经网络处理器"]}
        """
        self.nlp = spacy.load(model_name)
        self.synonym_mapping = synonym_mapping or {}

    def build(self, query: str) -> dict:
        doc = self.nlp(query)
        entities = []
        expanded_terms = []

        # 1. 实体识别
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
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
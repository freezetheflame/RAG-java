from data.build.tokenizer import ChineseTokenizer


def test_tokenizer():
    """测试分词器的功能"""
    tokenizer = ChineseTokenizer()
    text = "Java是一种广泛使用的编程语言。它具有跨平台性和高性能。"

    # 测试分词
    tokens = tokenizer.tokenize(text)
    assert len(tokens) > 0, "分词失败"

    # 测试关键词提取
    keywords = tokenizer.extract_keywords(text)
    assert len(keywords) > 0, "关键词提取失败"

    # 测试命名实体识别
    entities = tokenizer.named_entity_recognition(text)
    assert len(entities) > 0, "命名实体识别失败"
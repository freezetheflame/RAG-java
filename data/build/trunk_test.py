import random
import re

import pytest

from data.build.chunk import AdvancedChunker


def validate_chunk(chunk):
    """分块质量验证规则"""
    # 长度校验（按字符数）
    assert 600 <= len(chunk) <= 1500, f"分块长度异常: {len(chunk)}"

    # 完整性校验（检查截断）
    forbidden_patterns = [
        r"\w+[，。！？]$",  # 单词+标点结尾
        r"\d+\.[^0-9]$",  # 数字+点结尾（排除小数）
        r"[，、]$"  # 严格禁止的截断符
    ]

    # 允许自然句子结尾
    if re.search(r"[。！？]$", chunk):
        # 检查是否完整句子（包含主语谓语）
        has_subject = any(w in chunk for w in ["是", "有", "在", "可以"])
        has_predicate = any(w in chunk for w in ["了", "的", "着", "过"])
        if has_subject and has_predicate:
            return  # 允许自然句结尾

    for pattern in forbidden_patterns:
        assert not re.search(pattern, chunk), f"分块存在截断: {chunk[-20:]}"


@pytest.fixture
def sample_pdf():
    return "../data/分布式面试资料.pdf"


@pytest.fixture
def sample_md():
    return "../data/test.md"


def test_pdf_chunking(sample_pdf):
    chunker = AdvancedChunker()
    chunks = chunker.process_pdf(sample_pdf)

    # 基础断言
    assert len(chunks) >= 3, "PDF分块数量不足"
    # for chunk in chunks:
    #     validate_chunk(chunk)
    #     assert "Java" in chunk, "关键术语丢失"

    sample_indices = random.sample(range(len(chunks)), min(10, len(chunks)))
    for idx in sample_indices:
        validate_chunk(chunks[idx])

    # 检查表格保留
    assert any("|" in chunk for chunk in chunks), "表格数据丢失"


def test_markdown_chunking(sample_md):
    chunker = AdvancedChunker()
    chunks = chunker.process_markdown(sample_md)

    # 结构保留检查
    header_chunks = [c for c in chunks if c.startswith("# ")]
    assert len(header_chunks) >= 1, "Markdown标题未保留"

    # 代码块检查
    assert any("```java" in c for c in chunks), "代码块丢失"
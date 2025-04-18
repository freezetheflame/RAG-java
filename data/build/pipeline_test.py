import random
import re

import pytest

from data.build.chunk import AdvancedChunker
from data.build.pipeline import ProcessingPipeline


@pytest.fixture
def sample_pdf():
    return "../source/Bug.pdf"


@pytest.fixture
def sample_md():
    return "../data/test.md"


def test_pdf_chunking(sample_pdf):
    pipeline1 = ProcessingPipeline()
    chunks = pipeline1.process_document(sample_pdf)
    # 基础断言
    assert len(chunks) >= 3, "PDF分块数量不足"
    # 分词
    assert all("tokens" in chunk for chunk in chunks), "分词失败"





def test_markdown_chunking(sample_md):
    pipeline2 = ProcessingPipeline()
    chunks = pipeline2.process_document(sample_md)
    # 基础断言
    assert len(chunks) >= 3, "Markdown分块数量不足"
    # 分词
    assert all("tokens" in chunk for chunk in chunks), "分词失败"
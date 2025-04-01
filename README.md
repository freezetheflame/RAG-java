# RAG From Scratch

LLMs are trained on a large but fixed corpus of data, limiting their ability to reason about private or recent information. Fine-tuning is one way to mitigate this, but is often [not well-suited for facutal recall](https://www.anyscale.com/blog/fine-tuning-is-for-form-not-facts) and [can be costly](https://www.glean.com/blog/how-to-build-an-ai-assistant-for-the-enterprise).
Retrieval augmented generation (RAG) has emerged as a popular and powerful mechanism to expand an LLM's knowledge base, using documents retrieved from an external data source to ground the LLM generation via in-context learning. 
These notebooks accompany a [video playlist](https://youtube.com/playlist?list=PLfaIDFEXuae2LXbO1_PKyVJiQ23ZztA0x&feature=shared) that builds up an understanding of RAG from scratch, starting with the basics of indexing, retrieval, and generation. 
![rag_detail_v2](example.png)
 
根据上文的查询流程图，我们在迭代二中采取这样的设计
```shell
backend/
├── app/
│   ├── api/                # API接口层
│   │   ├── __init__.py
│   │   ├── endpoints/      # 路由定义
│   │   │   ├── __init__.py
│   │   │   ├── search.py   # 检索接口
│   │   │   └── document.py # 文档管理接口
│   │   └── dependencies.py # 依赖注入
│   ├── core/               # 核心逻辑
│   │   ├── __init__.py
│   │   ├── config.py       # 全局配置
│   │   ├── query/          # 查询处理模块
│   │   │   ├── __init__.py
│   │   │   ├── constructor.py  # 查询构造
│   │   │   ├── router.py       # 路由决策
│   │   │   └── translator.py   # 查询转换
│   │   └── retrieval/      # 检索增强模块
│   │       ├── __init__.py
│   │       ├── hybrid.py   # 混合检索
│   │       ├── rerank.py   # 结果重排序
│   │       └── cache.py    # 缓存策略
│   ├── db/                 # 数据库层
│   │   ├── __init__.py
│   │   ├── postgres.py     # PostgreSQL操作
│   │   ├── milvus.py       # Milvus向量操作
│   │   └── redis.py        # Redis缓存
│   ├── models/             # 数据模型
│   │   ├── __init__.py
│   │   ├── document.py     # 文档模型
│   │   └── response.py     # 响应模型
│   ├── pipelines/          # 数据处理流水线
│   │   ├── __init__.py
│   │   ├── parser.py       # 文档解析
│   │   ├── splitter.py     # 文本分块
│   │   └── vectorizer.py   # 向量化
│   ├── services/           # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── knowledge_base.py  # 知识库服务
│   │   └── llm       # LLM集成
│   │       ├── __init__.py
│   │       ├── factory.py  # LLM工厂
│   │       ├── ollama.py   # Ollama接口
│   │       └── deepseek.py # DeepSeek接口
│   └── main.py             # 应用入口
├── tests/                  # 测试用例
│   ├── __init__.py
│   ├── test_search.py
│   └── test_document.py
├── requirements.txt        # 依赖清单
├── Dockerfile              # 容器化配置
└── alembic/                # 数据库迁移
```

from .query_construction.query_factory import QueryFactory
from .query_routing.router_strategy import RouterStrategy
from .query_translation.marianmt_adapter import MarianMTTranslator


class QueryPipeline:
    def __init__(self):
        self.query_factory = QueryFactory()
        self.router_strategy = RouterStrategy()
        self.translator = MarianMTTranslator()

    def process(self, user_query: str, lang: str = "en"):
        # 1. Query Construction
        intent_constructor = self.query_factory.get_constructor("entity")
        query_context = intent_constructor.build(user_query)

        # 2. Translation (示例：中文→英文)
        if lang != "en":
            translated_query = self.translator.translate(user_query)
            query_context["translated_query"] = translated_query

        # 3. Routing
        router = self.router_strategy.select_router(query_context["intent"])
        retrieval_strategy = router.route(query_context)

        # 4. 返回最终检索策略和增强后的查询
        return {
            "strategy": retrieval_strategy,
            "query_context": query_context
        }
import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langchain_core.runnables import Runnable, RunnableConfig
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
from app.services.llm import LLMService
from app.api.dependency import get_llm_service_dependency


# 新增数据模型
class QuestionRecord(BaseModel):
    question_id: str
    session_id: str
    question_text: str
    stage: str
    is_followup: bool
    timestamp: datetime
    llm_provider: str


class LangChainAdapter(Runnable):
    """兼容最新LangChain的适配器"""

    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    @property
    def InputType(self):
        return str

    @property
    def OutputType(self):
        return str

    def invoke(self, input: str, config: Optional[RunnableConfig] = None) -> str:
        return self.llm_service.generate(input)

    async def ainvoke(self, input: str, config: Optional[RunnableConfig] = None) -> str:
        if hasattr(self.llm_service, 'agenerate'):
            return await self.llm_service.agenerate(input)
        return self.invoke(input, config)


class InterviewSession:
    def __init__(self, provider: str = "deepseek", position: str = "高级开发工程师"):
        self.llm_service = get_llm_service_dependency(provider)
        self.position = position

        # 配置LangChain
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=LangChainAdapter(self.llm_service),
            memory=self.memory,
            prompt=self._create_prompt_template(),
            verbose=True
        )

        # 会话管理
        self.session_id = self._generate_session_id()
        self.questions: List[QuestionRecord] = []
        self.evaluations: List[Dict] = []

    def _create_prompt_template(self) -> PromptTemplate:
        """创建标准化的提示模板"""
        return PromptTemplate(
            input_variables=["history", "input", "position", "stage"],
            template="""
            作为{position}职位的面试官，当前阶段：{stage}
            历史对话：{history}
            最新回答：{input}

            请：
            1. 生成专业评价（限100字）
            2. 提出下一个问题
            3. 判断是否需要追问

            返回JSON格式：
            {{
                "evaluation": "...",
                "next_question": "...",
                "need_followup": bool
            }}
            """
        )

    async def generate_question(self, last_answer: str = None) -> Dict:
        """生成问题并记录"""
        result = await self.chain.ainvoke({
            "input": last_answer or "",
            "position": self.position,
            "stage": self._get_current_stage()
        })

        try:
            data = json.loads(result.strip())
        except json.JSONDecodeError:
            data = self._fallback_response()

        # 记录问题
        question = QuestionRecord(
            question_id=str(uuid.uuid4()),
            session_id=self.session_id,
            question_text=data["next_question"],
            stage=self._get_current_stage(),
            is_followup=data.get("need_followup", False),
            timestamp=datetime.now(),
            llm_provider=self.llm_service.__class__.__name__
        )
        self.questions.append(question)

        return {
            "question_id": question.question_id,
            "question": question.question_text,
            **data
        }

    async def process_answer(self, answer: str) -> Dict:
        """处理用户回答并生成反馈"""
        # 将回答存入对话历史
        self.memory.save_context(
            {"input": answer},
            {"output": ""}
        )

        # 生成评价和新问题
        result = await self.generate_question(answer)

        # 保存评价记录
        self.evaluation_history.append({
            "answer": answer,
            "evaluation": result["evaluation"],
            "timestamp": datetime.now().isoformat()
        })

        return {
            "session_id": self.session_id,
            "evaluation": result["evaluation"],
            "next_question": result["question"],
            "need_followup": result["need_followup"]
        }

    def _get_current_stage(self) -> str:
        """根据问题历史判断当前阶段"""
        # 实现你的阶段判断逻辑
        if len(self.question_history) < 3:
            return "技术基础评估"
        return "项目经验评估"

    def _fallback_parse(self, raw_text: str) -> Dict:
        """应急响应解析"""
        return {
            "evaluation": "回答内容分析中...",
            "next_question": "能否详细说明这一点？",
            "need_followup": True
        }


class InterviewManager:
    def __init__(self):
        self.sessions: Dict[str, InterviewSession] = {}
        self.question_bank: List[QuestionRecord] = []

    def create_session(self, provider: str, position: str) -> str:
        session = InterviewSession(provider, position)
        self.sessions[session.session_id] = session
        return session.session_id

    def get_questions(self, session_id: str) -> List[Dict]:
        if session := self.sessions.get(session_id):
            return [q.dict() for q in session.questions]
        return []

    async def close_session(self, session_id: str) -> bool:
        if session := self.sessions.pop(session_id, None):
            self.question_bank.extend(session.questions)
            return True
        return False


# 异步测试用例
async def test_interview_flow():
    manager = InterviewManager()
    session_id = manager.create_session("deepseek", "Python工程师")

    session = manager.sessions[session_id]

    # 第一轮
    q1 = await session.generate_question()
    print(f"Q1: {q1['question']}")

    # 模拟回答
    a1 = "我熟悉Django和FastAPI"
    r1 = await session.process_answer(a1)
    print(f"反馈: {r1['evaluation']}")

    # 导出问题
    print("所有问题:", manager.get_questions(session_id))
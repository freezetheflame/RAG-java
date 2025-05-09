import json
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain_community.llms import HuggingFacePipeline
from langchain_community.chat_models import QianfanChatEndpoint
from openai import base_url, OpenAI

from app.config import Settings


class InterviewResponse(BaseModel):
    """面试回应的结构化输出"""
    evaluation: str = Field(description="对候选人回答的评价")
    next_question: str = Field(description="下一个面试问题")
    need_followup: bool = Field(description="是否需要深入追问")


class InterviewSession:
    """面试会话管理核心类"""

    def __init__(self, provider: str = "hunyuan"):
        # 初始化LLM
        self.llm = self._get_llm_by_provider(provider)
        # 配置对话链
        self.memory = ConversationBufferMemory()
        self.chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )

        # 面试状态管理
        self.session_id: str = self._generate_session_id()
        self.question_history: List[Dict] = []
        self.evaluation_history: List[Dict] = []
        self.position: str = "高级开发工程师"
        self.parser = JsonOutputParser(pydantic_object=InterviewResponse)

    def _get_llm_by_provider(self, provider: str):
        """根据提供商获取对应的LLM实例"""
        if provider == "openai":
            return ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo")
        elif provider == "qianfan":
            return QianfanChatEndpoint(model="ERNIE-Bot-4")
        elif provider == "deepseek":
            # 假设使用HuggingFace加载deepseek模型
            return  ChatOpenAI(openai_api_key=Settings.DEEPSEEK_API_KEY, base_url=base_url)
        elif provider == "hunyuan":
            # 为Hunyuan模型创建合适的接口 (如果有特定API)
            # 这里使用ChatOpenAI作为占位符，实际应根据hunyuan API调整
            return ChatOpenAI(model_name="hunyuan-lite",api_key=Settings.HUNYUAN_API_KEY, base_url="https://api.hunyuan.cloud.tencent.com/v1")
        else:
            # 默认使用OpenAI
            return ChatOpenAI(temperature=0.7)

    def _generate_session_id(self) -> str:
        # 生成会话ID
        return uuid.uuid4().hex

    def _build_interview_prompt(self, context: Dict) -> str:
        """构建面试提示模板"""
        return f"""
        你是一个专业的AI面试官，正在面试{context.get('position', '高级开发工程师')}职位的候选人。
        当前面试阶段：{context.get('current_stage', '技术能力评估')}
        已有问题：{" | ".join([q['question'] for q in self.question_history])[-500:] if self.question_history else "无"}
        最近回答：{context.get('last_answer', '无')}

        请根据以上上下文：
        1. 生成对最近回答的专业评价
        2. 提出下一个合适的面试问题
        3. 判断是否需要深入追问

        {self.parser.get_format_instructions()}
        """

    async def generate_question(self, last_answer: str = None) -> Dict:
        """生成面试问题和评价"""
        context = {
            "last_answer": last_answer,
            "current_stage": self._get_current_stage(),
            "position": self.position
        }

        # 使用LangChain管理对话流
        prompt = self._build_interview_prompt(context)
        response = await self.chain.arun(prompt)

        # 解析响应
        try:
            result_dict = self.parser.parse(response)
        except Exception:
            # 解析失败时使用后备方案
            result_dict = self._fallback_parse(response)

        # 更新历史记录
        self.question_history.append({
            "question": result_dict["next_question"],
            "timestamp": datetime.now().isoformat()
        })

        return {
            "question": result_dict["next_question"],
            "evaluation": result_dict.get("evaluation", ""),
            "need_followup": result_dict.get("need_followup", False)
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
        elif len(self.question_history) < 7:
            return "项目经验评估"
        else:
            return "深入技术探讨"

    def _fallback_parse(self, raw_text: str) -> Dict:
        """应急响应解析"""
        try:
            # 尝试寻找JSON格式的内容
            import re
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except:
            pass

        # 完全失败的情况下提供默认响应
        return {
            "evaluation": "回答内容分析中...",
            "next_question": "能否详细说明一下你的相关经验？",
            "need_followup": True
        }


class InterviewManager:
    """面试流程管理器（工厂模式）"""

    def __init__(self):
        self.active_sessions: Dict[str, InterviewSession] = {}

    def create_session(self, provider: str = "openai") -> str:
        """创建新面试会话"""
        session = InterviewSession(provider)
        self.active_sessions[session.session_id] = session
        return session.session_id

    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """获取已有会话"""
        return self.active_sessions.get(session_id)

    async def close_session(self, session_id: str):
        """结束并清理会话"""
        session = self.active_sessions.pop(session_id, None)
        if session:
            # 实现持久化逻辑
            pass
        return {"status": "success", "message": f"Session {session_id} closed"}


# 使用示例
async def demo_usage():
    manager = InterviewManager()
    session_id = manager.create_session("hunyuan")  # 这里可以选择不同的模型

    # 获取初始问题
    session = manager.get_session(session_id)
    first_question = await session.generate_question()
    print("初始问题:", first_question["question"])

    # 模拟用户回答
    user_answer = "我有5年全栈开发经验，主要使用Python和React，参与过多个大型项目的开发。"
    response = await session.process_answer(user_answer)

    print("面试官评价:", response["evaluation"])
    print("下一个问题:", response["next_question"])


if __name__ == "__main__":
    import asyncio

    asyncio.run(demo_usage())
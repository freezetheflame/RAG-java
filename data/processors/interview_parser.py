import re
from collections import defaultdict


class InterviewParser:
    def __init__(self):
        self.patterns = {
            "company": re.compile(r"【(.*?)】|公司[:：]\s*(\w+)"),
            "question": re.compile(r"题目\d+[:：](.*?)(?=题目\d+[:：]|答案\d+[:：]|$)", re.S),
            "answer": re.compile(r"答案\d+[:：](.*?)(?=题目\d+[:：]|答案\d+[:：]|$)", re.S)
        }

    def parse_content(self, text):
        """解析常见面试题格式"""
        result = defaultdict(list)

        # 提取公司信息
        if match := self.patterns["company"].search(text):
            result["company"] = match.group(1) or match.group(2)

        # 配对问题和答案
        questions = self.patterns["question"].findall(text)
        answers = self.patterns["answer"].findall(text)

        for q, a in zip(questions, answers):
            result["qa_pairs"].append({
                "question": q.strip(),
                "answer": self._clean_answer(a)
            })

        return dict(result)

    def _clean_answer(self, text):
        """标准化答案格式"""
        # 移除多余空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        # 代码块标准化
        return re.sub(r'```(?!java)', '```java', text)
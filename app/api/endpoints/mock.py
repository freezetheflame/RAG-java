from flask import Blueprint

bp = Blueprint('mock',__name__,url_prefix='/mock',)

bp.route('/question_list',methods = ['POST'])
def generate_questionList():
    """
    生成问题列表
    :return:
    """
    question_list = [
        {
            "question": "你好吗？",
            "answer": "我很好，谢谢！"
        },
        {
            "question": "你喜欢什么颜色？",
            "answer": "我喜欢蓝色。"
        },
        {
            "question": "你会做饭吗？",
            "answer": "我不会做饭，但我可以给你提供食谱。"
        }
    ]
    return question_list

bp.route('/get_next_question',methods = ['POST'])
def get_next_question():
    """
    获取下一个问题
    :return:
    """
    question = "你喜欢什么颜色？"
    return question
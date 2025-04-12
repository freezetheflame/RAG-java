from transformers import MarianMTModel, MarianTokenizer
from .base import Translator


class MarianMTTranslator(Translator):
    def __init__(self, model_name="Helsinki-NLP/opus-mt-zh-en"):
        model_path = "app/hfmodels/Helsinki-NLP"
        self.tokenizer = MarianTokenizer.from_pretrained(model_path)
        # self.tokenizer = MarianTokenizer.from_pretrained(model_name)
        # self.model = MarianMTModel.from_pretrained(model_name)
        self.model = MarianMTModel.from_pretrained(model_path)


    def translate(self, query: str, target_lang: str = "en") -> str:
        inputs = self.tokenizer(query, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
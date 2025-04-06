# app/utils/tokenizer.py
from sentence_transformers import SentenceTransformer

class Tokenizer:
    def __init__(self, model_name="sentence-transformers/paraphrase-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, text)-> list:
        return self.model.encode(text)
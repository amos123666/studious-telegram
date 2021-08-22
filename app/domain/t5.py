from .questionmatcher import AbstractQuestionMatcher
from transformers import AutoTokenizer, AutoModelWithLMHead


class T5(AbstractQuestionMatcher):

    def getSuggestions(self, question: str):
        tokenizer = AutoTokenizer.from_pretrained('t5-base')
        model = AutoModelWithLMHead.from_pretrained(
            't5-base', return_dict=True)

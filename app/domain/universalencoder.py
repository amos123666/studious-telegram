from .questionmatcher import AbstractQuestionMatcher
import time
import tensorflow as tf
import tensorflow_hub as hub
from scipy.spatial.distance import cosine
import operator
from transformers import AutoTokenizer, AutoModelWithLMHead

from typing import List

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


class UniversalEncoder(AbstractQuestionMatcher):
    MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"

    def __init__(self, questions):
        self.__model = hub.load(self.MODULE_URL)
        self.__summarise_model = AutoModelWithLMHead.from_pretrained(
            't5-base', return_dict=True)
        self.__tokenizer = AutoTokenizer.from_pretrained('t5-base')
        self.__questions = questions
        self.__question_list = list(questions.keys())
        #self.__sentence_embeddings = self.__model(self.__question_list)

    def getSummary(self, data):

        inputs = self.__tokenizer.encode(data,
                                         return_tensors='pt',
                                         max_length=512,
                                         truncation=True)

        summary_ids = self.__summarise_model.generate(
            inputs, no_repeat_ngram_size=2, max_length=20, min_length=10, length_penalty=5., num_beams=4, early_stopping=True)

        summary = self.__tokenizer.decode(
            summary_ids[0], skip_special_tokens=True)

        return summary

    def getSuggestions(self, question: str, type: str) -> List[str]:

        if type == 'Text_vec':
            question = question.split('.')
            summary = self.getSummary(question[1])
            question = question[0] + summary

        query_embedding = self.__model([question])[0]
        query_embedding = tf.reshape(query_embedding, (-1, 1))
        similarity_dict = {}

        for i, subject in enumerate(self.__questions.keys()):
            sentence_embedding = tf.reshape(
                self.__questions[subject][type], (-1, 1))
            similarity_dict[self.__question_list[i]] = 1 - \
                cosine(sentence_embedding, query_embedding)

        similarity_dict = sorted(similarity_dict.items(),
                                 key=operator.itemgetter(1), reverse=True)

        return [k[0] for k in similarity_dict]

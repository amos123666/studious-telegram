from .question import Question
from .questionmatcher import AbstractQuestionMatcher
from ..parser.parser import preprocess
import tensorflow as tf
import tensorflow_hub as hub
from scipy.spatial.distance import cosine
import operator

from typing import List, Tuple


class UniversalEncoder(AbstractQuestionMatcher):
    '''
    This is a class for sentence embedding of question subjects using Universal
    Sentence Encoder.
    '''
    MODULE_URL = "https://tfhub.dev/google/universal-sentence-encoder/4"

    def __init__(self):
        '''
        Constructor for the UniversalEncoder class.

        :param self: Instance of the UniversalEncoder object
        '''

        self.__model = hub.load(self.MODULE_URL)
        self.__questions: List[Question] = []
        self.__question_embeddings = []

    def addQuestions(self, questions: List[Question]) -> None:
        self.__questions += questions

        embeddings = self.__model([question.subject for question in questions])
        self.__question_embeddings += [tf.reshape(embedding, (-1, 1))
                                       for embedding in embeddings]

    def getSuggestions(self, question: str,
                       text_vec=True) -> List[Tuple[str, float]]:
        '''
        Determines question suggestions for a given question, based on the
        similarity of their subject-line.

        :param self: Instance of the UniversalEncoder object
        :param question: An element of the question dictionary
        :return [k[0] for k in similarity_dict]: List of all questions from
            question dictionary ordered from most similar to least
        '''
        # Pass the asked question into model to get embedding
        # question = preprocess(question)
        query_embedding = self.__model([question])[0]
        query_embedding = tf.reshape(query_embedding, (-1, 1))

        # Loop through the sentence embedding of each question, finding the cosine
        # between this and the embedding of the asked question
        suggestions = []
        for i, oldQuestion in enumerate(self.__questions):
            question_embedding = self.__question_embeddings[i]

            suggestions.append(
                (oldQuestion.subject,
                 1 -
                 cosine(
                     question_embedding,
                     query_embedding)))

        # Order dictionary to a list, such that higher cosines are first
        suggestions.sort(key=operator.itemgetter(1), reverse=True)

        return suggestions

from typing import List
from .domain.question import Question
from .interface import BasicCLI, TornadoWebInterface
from .domain import UniversalEncoder, SentBERT, Doc2Vec, T5
from .parser import parseQuestionsAnswersFromFile
from pathlib import Path


class App():

    def __init__(self, target_model: str, target_interface: str):

        questions, bodies = parseQuestionsAnswersFromFile(
            'app/testfiles/help2002-2017.txt')

        questionsObjects: List[Question] = []

        for i, question in enumerate(questions):
            questionsObjects.append(Question(question, bodies[i], []))

        if target_model == "UniversalEncoder":
            # Search for existing embeddings
            storageDir = Path('storage')

            if storageDir.exists() and storageDir.is_dir():
                for file in storageDir.iterdir():
                    if file.is_file() and target_model.lower() in file.name.lower():
                        print("Have embeddings file!")

            questionMatcher = UniversalEncoder()
        elif target_model == "BERT":
            questionMatcher = SentBERT()
        elif target_model == "doc2vec":
            questionMatcher = Doc2Vec()
        else:
            raise ValueError(f"targetModel ({target_model}) is not valid")

        questionMatcher.addQuestions(questions, bodies)

        if target_interface == "cli":
            summariser = T5()
            self.__interface = BasicCLI(
                questionMatcher, summariser, questions, target_model)
        elif target_interface == "web":
            self.__interface = TornadoWebInterface(
                8080, questionMatcher, questionsObjects)
        else:
            raise ValueError(
                f"target_interface ({target_interface}) is not valid")

    def start(self) -> None:
        self.__interface.start()

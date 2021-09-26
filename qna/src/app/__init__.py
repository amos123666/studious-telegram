from .interface import BasicCLI, WebInterface
from .domain import UniversalEncoder, SentBERT, Doc2Vec, T5
from .parser import parseQuestionsAnswersFromFile
from .parser import JsonLoader
import os


class App():

    def __init__(self, target_model, target_interface) -> None:

        if len(os.listdir("app/storage")) == 0:
            questions = parseQuestionsAnswersFromFile(
                'app/testfiles/help2002-2017.txt')

        if target_model == "UniversalEncoder":
            json = JsonLoader('app/storage/CITS2002_2021.json')
            questions = json.read_data()
            questionMatcher = UniversalEncoder(questions)
        elif target_model == "BERT":
            questionMatcher = SentBERT(questions)
        elif target_model == "doc2vec":
            questionMatcher = Doc2Vec(questions)
        else:
            raise ValueError(f"targetModel ({target_model}) is not valid")

        if target_interface == "cli":
            summariser = T5()
            self.__interface = BasicCLI(questionMatcher, summariser, questions)
        elif target_interface == "web":
            self.__interface = WebInterface(questionMatcher)
        else:
            raise ValueError(
                f"target_interface ({target_interface}) is not valid")

    def start(self) -> None:
        self.__interface.start()

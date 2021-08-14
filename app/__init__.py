from app.interface import BasicCLI
from app.domain import UniversalEncoder, questionmatcher
from app.embedder import SentEmbeddings
from app.parser import parseQuestionsAnswersFromFile
from app.storage import question_answers_to_json


class App():
    def __init__(self) -> None:
        questions, answers = parseQuestionsAnswersFromFile(
            'app/testfiles/help2002-2017.txt')
        question_answers_to_json(questions, answers)
        questionMatcher = UniversalEncoder(questions, answers)
        self.__cli = BasicCLI(questionMatcher)

    def start(self) -> None:
        self.__cli.start()

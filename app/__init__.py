from app.interface import BasicCLI
from app.domain import UniversalEncoder, questionmatcher
from app.embedder import SentEmbeddings
from app.parser import parseQuestionsAnswersFromFile
from app.parser import JsonLoader


class App():
    def __init__(self) -> None:
        # parseQuestionsAnswersFromFile(
        # 'app/testfiles/help2002-2017.txt')
        json = JsonLoader('questions.json')
        questions = json.read_data()
        questionMatcher = UniversalEncoder(questions)
        self.__cli = BasicCLI(questionMatcher, questions)

    def start(self) -> None:
        self.__cli.start()

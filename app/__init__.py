from app.interface import BasicCLI
from app.domain import UniversalEncoder, questionmatcher
from app.embedder import SentEmbeddings
from app.parser import parseQuestionsAnswersFromFile
from app.parser import JsonLoader


class App():
    def __init__(self) -> None:
        # parseQuestionsAnswersFromFile(
        # 'app/testfiles/help2002-2017.txt') Uncomment this if you want to create a new json file
        json = JsonLoader('app/storage/questions2017_UE.json')
        questions = json.read_data()
        questionMatcher = UniversalEncoder(questions)
        self.__cli = BasicCLI(questionMatcher, questions)

    def start(self) -> None:
        self.__cli.start()

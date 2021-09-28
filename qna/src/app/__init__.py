from .interface import BasicCLI, WebInterface
from .domain import UniversalEncoder, SentBERT, Doc2Vec, T5
from .parser import parseQuestionsAnswersFromFile
from pathlib import Path


class App():

    def __init__(self, target_model: str, target_interface: str):

        #         # If the diretory does not exists create one
        # if not os.path.exists('app/storage'):
        #     os.makedirs('app/storage')

        # # If we don't have any files already in the directory create
        # # based off the target_model
        # if len(os.listdir("app/storage")) == 0:
        #     questions = parseQuestionsAnswersFromFile(
        #         'app/testfiles/help2002-2017.txt', target_model)

        # # Find the first file that contains the target model
        # else:
        #     flag = False
        #     for file in os.listdir('app/storage'):
        #         if target_model in file:
        #             file = f'app/storage/{file}'
        #             json = JsonLoader(file)
        #             questions = json.read_data()
        #             flag = True
        #             break
        #     if not flag:
        #         questions = parseQuestionsAnswersFromFile(
        #             'app/testfiles/help2002-2017.txt', target_model)


        questions, bodies = parseQuestionsAnswersFromFile(
            'app/testfiles/help2002-2017.txt')

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
            self.__interface = WebInterface(questionMatcher)
        else:
            raise ValueError(
                f"target_interface ({target_interface}) is not valid")

    def start(self) -> None:
        self.__interface.start()

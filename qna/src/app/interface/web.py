import urllib.parse

import tornado.ioloop
import tornado.web

from .userinterface import AbstractUserInterface
from ..domain.questionmatcher import AbstractQuestionMatcher


class QuestionHandler(tornado.web.RequestHandler):
    def initialize(self, questionMatcher: AbstractQuestionMatcher) -> None:
        self.questionMatcher = questionMatcher

    def get(self, rawQuestion) -> None:
        question = urllib.parse.unquote(rawQuestion)

        suggestions = self.questionMatcher.getSuggestions(question, False)

        response = {
            "matches": [],
            "question": question
        }

        for suggestion in suggestions:
            response["matches"].append({
                "question": suggestion[0],
                "similarity": suggestion[1]
            })

        self.write(response)


class TornadoWebInterface(AbstractUserInterface):
    def __init__(self, port, questionMatcher: AbstractQuestionMatcher) -> None:
        super().__init__()

        self.__port = port
        self.__questionMatcher = questionMatcher

    def start(self) -> None:
        app = tornado.web.Application([
            (r"/api/question/([^/]+)", QuestionHandler, {"questionMatcher": self.__questionMatcher})
        ])

        app.listen(self.__port)

        print(f"Server started: http://localhost:{self.__port}")
        tornado.ioloop.IOLoop.current().start()

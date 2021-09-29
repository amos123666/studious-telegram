import re
from typing import Awaitable, Optional
import urllib.parse
import json

import tornado.ioloop
import tornado.web

from .userinterface import AbstractUserInterface
from ..domain.questionmatcher import AbstractQuestionMatcher


class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, questionMatcher: AbstractQuestionMatcher) -> None:
        self.questionMatcher = questionMatcher

    def prepare(self) -> Optional[Awaitable[None]]:
        if "Content-Type" not in self.request.headers:
            self.json_args = None
            return

        if self.request.headers["Content-Type"] != "application/json":
            self.json_args = None
            return

        self.json_args = json.loads(self.request.body)


class SuggestionHandler(BaseHandler):
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


class NewQuestionHandler(BaseHandler):
    def post(self) -> None:
        if self.json_args is None:
            self.set_status(400)
            return

        self.questionMatcher.addQuestions(
            [self.json_args['subject']], self.json_args['body'])

        self.set_status(200)


class TornadoWebInterface(AbstractUserInterface):
    def __init__(self, port, questionMatcher: AbstractQuestionMatcher) -> None:
        super().__init__()

        self.__port = port
        self.__questionMatcher = questionMatcher

    def start(self) -> None:
        app = tornado.web.Application([
            (r"/api/suggestion/([^/]+)", SuggestionHandler, {"questionMatcher": self.__questionMatcher}),
            (r"/api/question/new", NewQuestionHandler, {"questionMatcher": self.__questionMatcher}),
        ])

        app.listen(self.__port)

        print(f"Server started: http://localhost:{self.__port}")
        tornado.ioloop.IOLoop.current().start()

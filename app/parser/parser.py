from abc import ABC, abstractmethod


class AbstractLoader(ABC):
    def __init__(self, file):
        self.__file = file

    @abstractmethod
    def read_data(self):
        pass

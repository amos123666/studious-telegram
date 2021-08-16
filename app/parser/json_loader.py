from genericpath import isfile
import json
from .loader import AbstractLoader
import os


class JsonLoader(AbstractLoader):

    def __init__(self, file):
        self.__file = file

    def read_data(self):

        # load in json data
        if (os.path.isfile(self.__file)):
            with open(self.__file, 'r') as fp:
                try:
                    data = json.load(fp)
                except ValueError:
                    print("Invalid File. Must be extension '.json'")
                    return None
            return data
        else:
            print("File does not exists or directory does not exist")
            return None

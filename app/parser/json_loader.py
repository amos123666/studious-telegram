import json
from .loader import AbstractLoader


class JsonLoader(AbstractLoader):

    def read_data(file):

        # load in json data
        with open(file, 'r') as fp:
            data = json.load(fp)

        return data

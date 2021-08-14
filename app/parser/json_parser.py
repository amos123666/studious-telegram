import json
from .parser import AbstractLoader


class JsonLoader(AbstractLoader):

    def read_data(file):

        # load in json data
        with open(file, 'r') as fp:
            data = json.load(fp)

        # create dict and store json data
        dict_q = {}
        dict_q['questions'] = []
        for q in data['questions']:
            dict_q['questions'].append({
                'date': q['date'],
                'to': q['to'],
                'Received': q['Received'],
                'subject':  q['subject'],
                'from': q['from'],
                'x-smilie': q['x-smilie'],
                'x-img': q['x-img'],
                'text_body': q['text_body'],
                'subject_embedding': q['subject_embedding'],
                'text_embedding': q['text_embedding'],
                'answers': q['answers']
            })
        return dict_q

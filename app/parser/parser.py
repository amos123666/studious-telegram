import email
import tensorflow as tf
import tensorflow_hub as hub
from transformers import AutoTokenizer, AutoModelWithLMHead
import json


def parseQuestionsAnswersFromFile(filePath: str):
    '''
    Returns a dictionary containing each question in filePath, and a 
    dictionary containing each answer in filePath.

    :param filePath: File to be parsed
    :return questions: Dictionary of question threads
    :return answers: Dictionary of answer threads
    '''
    threads = parseThreadsFromFile(filePath)
    getPostsFromThreads(threads)


def parseThreadsFromFile(filePath: str):
    '''
    Arranges the contents of a file into separate threads (ie. an individual 
    question or answer) that are stored as list items.

    :param filePath: File to be parsed
    :return threads: List of question/answer strings
    '''
    with open(filePath, 'r') as file:
        line = file.readline()
        line = file.readline()  # Not sure best way to do this, needed to skip the first line
        str = ''
        threads = []

        while line:
            # a date line indicates a new question/answer
            if(line[:4] == 'Date' and len(str) > 0):
                str = str.rstrip('\n')
                threads.append(str)
                str = ''
            str += line
            line = file.readline()
        threads.append(str)
    return threads


def getPostsFromThreads(threads):
    '''
    For each item in a given threads list, a list containing all contents
    is stored in a json formatted dictionary to be stored in a JSON file

    :param threads: List of question/answer strings
    :return None:
    '''
    questions = {}

    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained(
        't5-base', return_dict=True)

    for i in range(0, len(threads)):

        msg = email.message_from_string(threads[i])
        print(msg['Subject'])
        if msg['Subject'] not in questions.keys():
            subj_vec = get_vectors(msg['Subject'])
            subj_vec = subj_vec.numpy().tolist()

            text_vec = text_summarisation(msg._payload, tokenizer, model)
            text_vec = get_vectors(str(msg['Subject'] + text_vec))
            text_vec = text_vec.numpy().tolist()
            questions[msg['Subject']] = {'Date': msg['Date'],
                                         'To': msg['To'],
                                         'Received': msg['Received'],
                                         'Subject_vec': subj_vec,
                                         'From': msg['From'],
                                         'X-smile': msg['X-smile'],
                                         'X-img': msg['X-img'],
                                         'Text': msg._payload,
                                         'Text_vec': text_vec,
                                         'Answers': [],
                                         }
        else:
            questions[msg['Subject']]['Answers'].append({'Date': msg['Date'],
                                                         'To': msg['To'],
                                                         'Received': msg['Received'],
                                                         'Subject': msg['Subject'],
                                                         'From': msg['From'],
                                                         'X-smile': msg['X-smile'],
                                                         'X-img': msg['X-img'],
                                                         'Text': msg._payload,
                                                         })
    with open('app/storage/questions2017_UE_test.json', 'w') as outfile:
        json.dump(questions, outfile, indent=4)
    print("Finished loading Json...")


def get_vectors(question):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    vec = model([question])[0]
    vec = tf.reshape(vec, (-1, 1))
    return vec


def text_summarisation(data, tokenizer, model):

    inputs = tokenizer.encode(data,
                              return_tensors='pt',
                              max_length=512,
                              truncation=True)

    summary_ids = model.generate(
        inputs, no_repeat_ngram_size=2, max_length=20, min_length=10, length_penalty=5., num_beams=4, early_stopping=True)

    summary = tokenizer.decode(
        summary_ids[0], skip_special_tokens=True)

    return summary

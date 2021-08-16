import email
from genericpath import isdir
import tensorflow as tf
import tensorflow_hub as hub
import json
import os


def parseQuestionsAnswersFromFile(filePath: str):
    '''
    Returns a dictionary containing each question in filePath, and a
    dictionary containing each answer in filePath.

    :param filePath: File to be parsed
    :return questions: Dictionary of question threads
    :return answers: Dictionary of answer threads
    '''
    threads = parseThreadsFromFile(filePath)
    # getPostsFromThreads(threads)


def parseThreadsFromFile(filePath: str):
    '''
    Arranges the contents of a file into separate threads (ie. an individual
    question or answer) that are stored as list items.

    :param filePath: File to be parsed
    :return threads: List of question/answer strings
    '''
    if(os.path.isfile(filePath) or os.path.isdir(filePath)):

        with open(filePath, 'r') as file:
            try:
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

            except FileNotFoundError:
                print("File can not be found.")
    else:
        print("File or directory does not exists.")


def getPostsFromThreads(threads):
    '''
    For each item in a given threads list, a list containing all contents
    is stored in a json formatted dictionary to be stored in a JSON file

    :param threads: List of question/answer strings
    :return None:
    '''
    questions = {}

    for i in range(0, len(threads)):

        msg = email.message_from_string(threads[i])

        if msg['Subject'] not in questions.keys():
            if(msg['X-anonymous'] == "yes"):
                anonymous = "yes"
            else:
                anonymous = "no"
            vec = get_vectors(msg['Subject'])
            questions[msg['Subject']] = {'Date': msg['Date'],
                                         'To': msg['To'],
                                         'Received': msg['Received'],
                                         'Subject_vec': vec,
                                         'From': msg['From'],
                                         'X-smile': msg['X-smile'],
                                         'X-img': msg['X-img'],
                                         'X-anonymous': anonymous,
                                         'Text': msg._payload,
                                         'Text_vec': [0],
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
                                                         'X-anonymous': anonymous,
                                                         'Text': msg._payload,
                                                         })
    with open('app/storage/questions2017_UE.json', 'w') as outfile:
        json.dump(questions, outfile, indent=4)
    print("Finished loading Json...")


def get_vectors(question):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    vec = model([question])[0]
    vec = tf.reshape(vec, (-1, 1))
    vec = vec.numpy().tolist()
    print(type(vec))
    return vec

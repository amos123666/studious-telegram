import email
import tensorflow as tf
import tensorflow_hub as hub
import json
from transformers import T5ForConditionalGeneration, T5Tokenizer
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import numpy as np
import time


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

    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    print("Finished Loading Universal Encoder")
    embeddings_questions = model(
        [email.message_from_string(i)['Subject'] for i in threads])
    print("Finished Universal Encoder Embeddings")

    model2 = T5ForConditionalGeneration.from_pretrained("t5-small")
    tokenizer = T5Tokenizer.from_pretrained("t5-small")
    print("Finished Loading T5 model")

    start = time.time()
    embeddings_text = model([email.message_from_string(i)['Subject'] + get_summarisation(
        email.message_from_string(i)._payload, tokenizer, model2) for i in threads])
    end = time.time() - start
    print(end)
    print("Finished t5 Embeddings")

    questions = {}

    for i in range(0, len(threads)):

        msg = email.message_from_string(threads[i])

        if msg['Subject'] not in questions.keys():

            text_vec = embeddings_text[i].numpy().tolist()
            vec = embeddings_questions[i].numpy().tolist()

            questions[msg['Subject']] = {'Date': msg['Date'],
                                         'To': msg['To'],
                                         'Received': msg['Received'],
                                         'Subject_vec': vec,
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
    with open('app/storage/questions2017_Universal_Encoder.json', 'w') as outfile:
        json.dump(questions, outfile, indent=4)
    print("Finished loading Json...")


def get_summarisation(data, tokenizer, model):
    input = tokenizer.encode(data, return_tensors="pt",
                             max_length=512, truncation=True)
    # generate the summarization output
    outputs = model.generate(
        input,
        max_length=50,
        min_length=30,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True)
    # just for debugging
    return tokenizer.decode(outputs[0])


def preprocess(data):
    '''
    # I still don't know if I will use htis now.
    '''

    # Tokenize question and remove punctuation and lower strings
    data = word_tokenize(data)
    data = [i for i in data if i not in string.punctuation]
    data = [i.lower() for i in data]

    # Convert words to stem form
    # e.g. 'playing' is converted to 'play'
    lemmatizer = WordNetLemmatizer()
    data = [lemmatizer.lemmatize(i) for i in data]

    # Remove stopwords as they don't add value to the sentence meaning
    # and select only the top 10 stop words.
    # e.g. 'the' is not a valuable word
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords = stopwords[0:10]
    data = [i for i in data if i not in stopwords]

    return "".jdata

import email
import tensorflow as tf
import tensorflow_hub as hub
import json


def parseQuestionsAnswersFromFile(filePath: str):
    threads = parseThreadsFromFile(filePath)
    getPostsFromThreads(threads)
    # questions, answers = parseQuestionsAnswersFromPosts(posts)
    # return questions, answers


def parseThreadsFromFile(filePath: str):
    with open(filePath, 'r') as file:
        line = file.readline()
        line = file.readline()  # Not sure best way to do this, needed to skip the first line
        str = ''
        threads = []

        while line:
            if(line[:4] == 'Date' and len(str) > 0):
                str = str.rstrip('\n')
                threads.append(str)
                str = ''
            str += line
            line = file.readline()
        threads.append(str)
    return threads


def getPostsFromThreads(threads):
    questions = {}
    for i in range(0, len(threads)):

        msg = email.message_from_string(threads[i])

        if msg['Subject'] not in questions.keys():

            vec = get_vectors(msg['Subject'])
            vec = vec.numpy().tolist()
            questions[msg['Subject']] = {'Date': msg['Date'],
                                         'To': msg['To'],
                                         'Received': msg['Received'],
                                         'Subject_vec': vec,
                                         'From': msg['From'],
                                         'X-smile': msg['X-smile'],
                                         'X-img': msg['X-img'],
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
                                                         'Text': msg._payload,
                                                         })
    with open('questions2017_UE.json', 'w') as outfile:
        json.dump(questions, outfile, indent=4)
    print("Finished loading Json...")


def get_vectors(question):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    vec = model([question])[0]
    vec = tf.reshape(vec, (-1, 1))
    return vec

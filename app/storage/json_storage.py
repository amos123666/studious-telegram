import tensorflow as tf
import tensorflow_hub as hub
from scipy.spatial.distance import cosine
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from sentence_transformers import SentenceTransformer
import json
import operator

from typing import List
import numpy as np


def question_answers_to_json(questions, answers):
    store_questions_json(questions, answers)


def store_questions_json(questions, answers):

    # Data to store
    data = {}
    data['questions'] = []

    # Get all the vectors for subject and text_summation
    flag = False
    i = 0
    for k, v in questions.items():

        # get subject vectors
        subject_vec = get_vectors(k)
        subject_vec = subject_vec.numpy().tolist()

        # get summary vetors
        summary = get_summary(v[6])
        text_vec = get_vectors(summary)
        text_vec = text_vec.numpy().tolist()

        # store question in dict for json storage
        data['questions'].append({
            'date': v[0],
            'to': v[1],
            'Received': v[2],
            'subject':  k,
            'from': v[3],
            'x-smilie': v[4],
            'x-img': v[5],
            'text_body': v[6],
            'subject_embedding': subject_vec,
            'text_embedding': text_vec,
            'answers': [],
        })

        # store answers inside 'answers' key for the question
        ans = answers.get(k)
        for a in ans:
            data['questions'][i]['answers'].append({
                'date': a[0],
                'to': a[1],
                'Received': a[2],
                'subject':  k,
                'from': a[3],
                'x-smilie': a[4],
                'x-img': a[5],
                'text_body': a[6],
            })
        i += 1

    # write to file
    with open('questions_UE.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def get_vectors(data):
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    model = hub.load(module_url)
    vec = model([data])[0]
    vec = tf.reshape(vec, (-1, 1))
    return vec


def get_summary(data):
    tokenizer = AutoTokenizer.from_pretrained('t5-base')
    model = AutoModelWithLMHead.from_pretrained(
        't5-base', return_dict=True)

    inputs = tokenizer.encode(data,
                              return_tensors='pt',
                              max_length=512,
                              truncation=True,
                              )

    summary_ids = model.generate(inputs,
                                 max_length=50,
                                 min_length=10,
                                 length_penalty=5.,
                                 num_beams=2)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

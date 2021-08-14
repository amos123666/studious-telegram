import os
import email


'''
This method takes in a text file and separates the file by posts
@param: file - the text file
@return: threads - list of posts
'''


def parsing_data(file):
    parsed_threads = []

    try:
        data_file = open(file, 'r')
    except Exception as e:
        print("Error opening file: " + e)

    cur_par = ''
    for line in data_file:
        if 'Date' in line and cur_par:
            if cur_par.strip() != '': #empty email check
                parsed_threads.append(cur_par)
            cur_par = ''
            cur_par += line
        else:
            cur_par += line

    data_file.close()

    return parsed


'''
This method breaks each post down into managable data structure
so that each specific component can be extracted easily
@param: threads - the list of psots
@return: posts - list of lists that contains separated components of each post
'''


def get_posts(threads):
    posts = []
    for i in range(0, len(threads)):
        msg = email.message_from_string(threads[i])
        p = []
        p.append(msg['Date'])
        p.append(msg['Subject'])
        p.append(msg._payload)
        posts.append(p)
    return posts


'''
This method converts posts into a dictionary data structure for
easier extraction of post components
@param: posts - the list of posts
@return: question - the dictionary of questions asked
         answers - the dicitonary of answers to the question

'''


def create_data_structures(posts):
    dict_q = {}
    dict_a = {}
    for i in range(len(posts)):
        li = []
        if posts[i][1] not in dict_q:
            li.append(posts[i][0])
            li.append(posts[i][2])
            dict_q[posts[i][1]] = li
            dict_a[posts[i][1]] = []
        else:
            li.append(posts[i][0])
            li.append(posts[i][2])
            val = dict_a.get(posts[i][1])
            val.append(li)
            dict_a[posts[i][1]] = val
    return dict_q, dict_a


def main():
    file = 'help2002-2017.txt'
    parsed_list = parsing_data(file)
    posts = get_posts(parsed_list)
    questions, answers = create_data_structures(posts)
    print("SUBJECTS:")
    print()
    for k, v in questions.items():
        print(f'QUESTION: {k}')
        ans = answers.get(k)
        print()
        print('ANSWERS')
        print('--------')
        for a in ans:
            print(a[1] + '\n\n')
            print('-----')
        print('----------------------')


if __name__ == "__main__":
    main()

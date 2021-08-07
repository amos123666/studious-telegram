import os
import email

os.chdir('F:\FAQ_Project_data')  # REMOVE THIS

'''
This method takes in a text file and separates the file by posts
@param: file - the text file
@return: threads - list of posts
'''


def parsing_data(file):
    with open(file, 'r') as f:
        line = f.readline()
        line = f.readline()  # Not sure best way to do this, needed to skip the first line
        str = ''
        threads = []

        while line:
            if(line[:4] == 'Date' and len(str) > 0):
                str = str.rstrip('\n')
                threads.append(str)
                str = ''
            str += line
            line = f.readline()
        threads.append(str)
    return threads


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

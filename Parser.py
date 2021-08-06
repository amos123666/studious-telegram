import os
import email

os.chdir('F:\FAQ_Project_data')  # REMOVE THIS


def parsing_data(file):
    with open(file, 'r') as f:
        line = f.readline()
        line = f.readline()  # Not sure best way to do this, needed to skip the first line
        str = ''
        threads = []

        while line:
            if(line[:4] == 'Date' and len(str) > 1):
                threads.append(str)
                str = ''
            str += line
            line = f.readline()
    return threads


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


def create_data_structures(posts):
    dict_q = {}
    dict_a = {}
    for i in range(len(posts)):
        li = []
        if posts[i][1] not in dict_q:
            li.append(posts[i][0])
            li.append(posts[i][2])
            dict_q[posts[i][1]] = li
        else:
            if posts[i][1] not in dict_a:
                li.append(posts[i][0])
                li.append(posts[i][2])
                dict_a[posts[i][1]] = li
            else:
                li.append(posts[i][0])
                li.append(posts[i][2])
                current_li = dict_a.get(posts[i][1])
                new_li = current_li+li
                dict_a[posts[i][1]] = new_li
    return dict_q, dict_a


def main():
    file = 'help2002-2017.txt'
    parsed_list = parsing_data(file)
    posts = get_posts(parsed_list)
    questions, answers = create_data_structures(posts)
    print("SUBJECTS:")
    print()
    for k, v in questions.items():
        print(k)


if __name__ == "__main__":
    main()

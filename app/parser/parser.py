import email


def parseQuestionsAnswersFromFile(filePath: str):
    threads = parseThreadsFromFile(filePath)
    posts = getPostsFromThreads(threads)
    print(posts[0])
    #questions, answers = parseQuestionsAnswersFromPosts(posts)

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
    posts = []
    for i in range(0, len(threads)):
        msg = email.message_from_string(threads[i])
        p = []
        p.append(msg['Date'])
        p.append(msg['To'])
        p.append(msg['Received'])
        p.append(msg['Subject'])
        p.append(msg['From'])
        p.append(msg['X-smile'])
        p.append(msg['X-img'])
        p.append(msg._payload)
        posts.append(p)
    return posts


def parseQuestionsAnswersFromPosts(posts):
    dict_q = {}
    dict_a = {}
    for i in range(len(posts)):
        li = []
        if posts[i][3] not in dict_q:  # post[i][3] == Subject
            li.append(posts[i][0])  # Date
            li.append(posts[i][1])  # To
            li.append(posts[i][2])  # Received
            li.append(posts[i][4])  # From
            li.append(posts[i][5])  # X-smile
            li.append(posts[i][6])  # X-img
            li.append(posts[i][7])  # text body
            dict_q[posts[i][3]] = li
            dict_a[posts[i][3]] = []
        else:
            li.append(posts[i][0])  # Date
            li.append(posts[i][1])  # To
            li.append(posts[i][2])  # Received
            li.append(posts[i][4])  # From
            li.append(posts[i][5])  # X-smile
            li.append(posts[i][6])  # X-img
            li.append(posts[i][7])  # text body
            val = dict_a.get(posts[i][3])
            val.append(li)
            dict_a[posts[i][3]] = val
    return dict_q, dict_a

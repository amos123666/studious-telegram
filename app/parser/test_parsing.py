import unittest
from parsing import get_vectors, parseThreadsFromFile, getPostsFromThreads
import json


class TestParsing(unittest.TestCase):

    def test_vectors(self):
        '''
        Tests when inputting a string, that the resulting vector
        is an instance of the class list, and the length is 512
        '''
        string = "I need exam help."
        actual = get_vectors(string)

        self.assertEqual(isinstance(actual, list), True)
        self.assertEqual(len(actual), 512)

    def test_parsing_testfiles(self):
        '''
        Tests when reading in a file, the output is a list of strings containing
        each individual post as its element
        '''

        file = 'testposts.txt'
        actual = parseThreadsFromFile(file)

        expected1 = "Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone,\n\nI've asked the LCS/Echo360 Gods to permit our unit's recordings to be available from \noutside Blackboard, and accessible from our webpage's left-hand margin without requiring \nyou to login to Blackboard (as it's been in previous years).\n\nUntil then, you can access last Tuesday's lecture via Blackboard (ho hum!).\n\nChris."
        print(len(actual[0]))
        print(len(expected1))
        self.assertEqual(actual[0], expected1)

    def test_create_json(self):
        '''
        Tests to observe how JSON formatted dictionary is created and
        whether the contents are in the correct format.
        '''
        text = ["Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone,\n\nI've asked the LCS/Echo360 Gods to permit our unit's recordings to be available from \noutside Blackboard, and accessible from our webpage's left-hand margin without requiring \nyou to login to Blackboard (as it's been in previous years).\n\nUntil then, you can access last Tuesday's lecture via Blackboard (ho hum!).\n\nChris.", "Date: Thu Aug  3 18:59:12 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nYou may now access our LCS recordings directly, from the left margin of our unit's webpage, without \nneeding to go through LMS.  Thanks to those that reported \
                the problem."]
        actual = getPostsFromThreads(text)

        with open('testfile2.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(actual, expected)

    def test_all_components(self):
        '''
        Tests all components of the parsing file to observer functionality
        between functions and how each are handled in sequence
        '''

        file = 'testposts.txt'
        threads = parseThreadsFromFile(file)
        actual = getPostsFromThreads(threads)

        with open('testfile2.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()

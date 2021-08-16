import unittest
from parsing import get_vectors, parseThreadsFromFile


class TestJParsing(unittest.TestCase):

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

        expected1 = 'Date: Mon Jul 31 12:17:48 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 130.95.1.70\nSubject: Hello Everyone, welcome to CITS2002 Systems Programming in 2017\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone, welcome to CITS2002 Systems Programming in 2017.\n\nThanks, Chris.\n\n'
        print(len(actual[0]))
        print(len(expected1))
        self.assertEqual(actual[0], expected1)


if __name__ == '__main__':
    unittest.main()

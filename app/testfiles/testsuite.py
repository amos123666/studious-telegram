
import unittest
from app.parser.json_loader import JsonLoader
from app.parser.parsing import get_vectors, parseThreadsFromFile, getPostsFromThreads
from app.domain import UniversalEncoder, SentBERT
import json
from time import perf_counter


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

        string2 = ""
        actual2 = get_vectors(string2)
        self.assertEqual(actual2, None)

    def test_parsing_testfiles(self):
        '''
        Tests when reading in a file, the output is a list of strings containing
        each individual post as its elements
        '''

        file = 'app/testfiles/testparsingfiles/testposts.txt'
        actual = parseThreadsFromFile(file)

        expected1 = "Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone,\n\nI've asked the LCS/Echo360 Gods to permit our unit's recordings to be available from \noutside Blackboard, and accessible from our webpage's left-hand margin without requiring \nyou to login to Blackboard (as it's been in previous years).\n\nUntil then, you can access last Tuesday's lecture via Blackboard (ho hum!).\n\nChris."
        self.assertEqual(actual[0], expected1)

    def test_create_json(self):
        '''
        Tests to observe how JSON formatted dictionary is created and
        whether the contents are in the correct format.
        '''

        text = ["Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone,\n\nI've asked the LCS/Echo360 Gods to permit our unit's recordings to be available from \noutside Blackboard, and accessible from our webpage's left-hand margin without requiring \nyou to login to Blackboard (as it's been in previous years).\n\nUntil then, you can access last Tuesday's lecture via Blackboard (ho hum!).\n\nChris.", "Date: Thu Aug  3 18:59:12 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nYou may now access our LCS recordings directly, from the left margin of our unit's webpage, without \nneeding to go through LMS.  Thanks to those that reported \
                the problem."]
        actual = getPostsFromThreads(text)

        with open('app/testfiles/testparsingfiles/questions2017_UE.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(self.ordered(actual), self.ordered(expected))

    def ordered(self, obj):
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    def test_all_components(self):
        '''
        Tests all components of the parsing file to observe functionality
        between functions and how each is handled in sequence to create a
        correctly formatted JSON object.
        '''

        file = 'app/testfiles/testparsingfiles/testposts.txt'
        threads = parseThreadsFromFile(file)
        actual = getPostsFromThreads(threads)

        with open('app/testfiles/testparsingfiles/testfile2.json', 'r') as fp:
            expected = json.load(fp)

        self.assertEqual(actual, expected)  # -------------------------


class TestJson(unittest.TestCase):

    def test_json_storage(self):
        '''
        Tests to observer how the function successfully creates
        a JSON object when reading in a file with JSON data.
        '''

        file = 'app/testfiles/testparsingfiles/testfile1.json'
        json = JsonLoader(file)
        actual1 = json.read_data()

        for subject in actual1.keys():

            self.assertEqual(actual1[subject]['Date'],
                             'Wed Nov  1 13:07:21 2017')
            self.assertEqual(actual1[subject]['To'],
                             'help2002@csse.uwa.edu.au')
            self.assertEqual(
                actual1[subject]['Received'], 'from 101.177.104.187')
            self.assertEqual(subject,
                             'part 5 clarification')
            self.assertEqual(actual1[subject]['From'],
                             'poster033@student.uwa.edu.au')
            self.assertEqual(actual1[subject]['X-smile'], None)
            self.assertEqual(actual1[subject]['X-img'], 'none')
            self.assertEqual(actual1[subject]['X-anonymous'], 'no')
            self.assertEqual(actual1[subject]['Text_vec'], [0])
            self.assertEqual(len(actual1[subject]['Answers']), 3)

    def test_file_exists(self):
        '''
        Tests to observer how the function handles files that
        do no exists or the director is incorrect during execution
        '''

        start = perf_counter()

        file = "app/testfiles/testparsingfiles/TestFileExists.json"

        json = JsonLoader(file)
        actual1 = json.read_data()

        self.assertEqual(actual1, None)

    def test_file_json_readable(self):
        '''
        Tests to observer how the function handles non JSON readable
        data or invalid file formats for JSON extraction
        '''

        file = 'app/testfiles/testparsingfiles/testfile.jpg'

        json = JsonLoader(file)
        actual1 = json.read_data()

        self.assertEqual(actual1, None)


class TestModels(unittest.TestCase):

    def test_get_suggetions_Universal_Encoder(self):

        string = ''
        test_questions = 'app/testfiles/testparsingfiles/testfile2.json'
        json_obj = JsonLoader(test_questions)
        questions = json_obj.read_data()
        encoder = UniversalEncoder(questions)
        suggestions1 = encoder.getSuggestions(string)

        self.assertEquals(suggestions1, None)

        string2 = 'plchatazpyiiihbkyisyamgfixbdiukplyeukfzeuoeyhzdlensohptbznnmggkwbkjyutpjjmvvz \
                   bozqdnyaefklodvpqvpqgboxtxulgixcejjuzxyqfwmfncjpirzerujaqrkhvrigmdhaylyzxayel \
                   kjepsevpqjgyctqzckmjrxuompdqyxpogpudjafupzlrqjxpkffqabxrohufolacipnrrrmkxovoyf \
                   jhjikhidwwehxwritzrztzpjovqyluzivpmbdhtlxazuqwdikadrnfhkaiugvcdbiczkzgxbaidbnj \
                   xqrwzozduwhwvneutchghmbjiyhqrvvvdazvuvceyavaystjqccjtnxadmnrlxahqsqjnlkovupwfd \
                   rwmiwziuiovagthhafaogavwcsrcpbglnlcrncsmuvfcoleirwpdbdijbsmugypucsjelemvgqlddbi \
                   vbqgajyjcxtgmwklbutzcnqcftluwslcabsgwhlagpegjz'

        encoder2 = UniversalEncoder(questions)
        suggestions2 = encoder2.getSuggestions(string)
        self.assertEquals(suggestions2, None)

    def test_get_suggetions_Sent_BERT(self):

        string = ''
        test_questions = 'app/testfiles/testparsingfiles/testfile2.json'
        json_obj = JsonLoader(test_questions)
        questions = json_obj.read_data()
        encoder = SentBERT(questions)
        suggestions1 = encoder.getSuggestions(string)

        self.assertEquals(suggestions1, None)

        string2 = 'plchatazpyiiihbkyisyamgfixbdiukplyeukfzeuoeyhzdlensohptbznnmggkwbkjyutpjjmvvz \
                   bozqdnyaefklodvpqvpqgboxtxulgixcejjuzxyqfwmfncjpirzerujaqrkhvrigmdhaylyzxayel \
                   kjepsevpqjgyctqzckmjrxuompdqyxpogpudjafupzlrqjxpkffqabxrohufolacipnrrrmkxovoyf \
                   jhjikhidwwehxwritzrztzpjovqyluzivpmbdhtlxazuqwdikadrnfhkaiugvcdbiczkzgxbaidbnj \
                   xqrwzozduwhwvneutchghmbjiyhqrvvvdazvuvceyavaystjqccjtnxadmnrlxahqsqjnlkovupwfd \
                   rwmiwziuiovagthhafaogavwcsrcpbglnlcrncsmuvfcoleirwpdbdijbsmugypucsjelemvgqlddbi \
                   vbqgajyjcxtgmwklbutzcnqcftluwslcabsgwhlagpegjzg'

        encoder2 = SentBERT(questions)
        suggestions2 = encoder2.getSuggestions(string)
        self.assertEquals(suggestions2, None)


def run_some_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [TestJson, TestParsing, TestModels]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()

    results = runner.run(big_suite)


if __name__ == '__main__':
    run_some_tests()

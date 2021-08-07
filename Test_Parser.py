import unittest
import Parser


class TestPostParser(unittest.TestCase):
    def test_text_parser(self):
        print("BEGIN TESTING BLOCK 1: test_text_parser")
        print()

        print("UNIT1: test file 1")
        file = "test_parser.txt"
        actual = Parser.parsing_data(file)
        expected1 = "Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nHello Everyone,\n\nI've asked the LCS/Echo360 Gods to permit our unit's recordings to be available from \noutside Blackboard, and accessible from our webpage's left-hand margin without requiring \nyou to login to Blackboard (as it's been in previous years).\n\nUntil then, you can access last Tuesday's lecture via Blackboard (ho hum!).\n\nChris."
        expected2 = "Date: Thu Aug  3 18:59:12 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nYou may now access our LCS recordings directly, from the left margin of our unit's webpage, without \nneeding to go through LMS.  Thanks to those that reported the problem."
        self.assertEqual(
            actual[0], expected1)
        self.assertEqual(
            actual[1], expected2)
        print()

    def test_post_converter(self):
        print("BEGIN TESTING BLOCK 2: test_post_converter")
        print()

        print("UNIT1: 2 posts")
        test_list = ["Date: Wed Aug  2 18:26:40 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nTesting1\n\nComplete.",
                     "Date: Thu Aug  3 18:59:12 2017\nTo: help2002@csse.uwa.edu.au\nReceived: from 106.68.103.155\nSubject: On lecture recordings\nFrom: chris.mcdonald@uwa.edu.au\nX-smilie: none\nX-img: none\n\nTesting2\n\nComplete."]
        actual = Parser.get_posts(test_list)
        expected = [['Wed Aug  2 18:26:40 2017', 'On lecture recordings',
                    'Testing1\n\nComplete.'], ['Thu Aug  3 18:59:12 2017', 'On lecture recordings', 'Testing2\n\nComplete.']]
        self.assertEqual(
            actual[0], expected[0])
        self.assertEqual(
            actual[1], expected[1])
        print()

    def test_data_structure(self):
        print("BEGIN TESTING BLOCK 3: test_data_strutures")
        print()

        print("UNIT1: 1 question, 1 answer")
        test_posts = [['Wed Aug  2 18:26:40 2017', 'On lecture recordings',
                       'Testing1\n\nComplete.'], ['Thu Aug  3 18:59:12 2017', 'On lecture recordings', 'Testing2\n\nComplete.']]
        actual_q, actual_a = Parser.create_data_structures(test_posts)
        expected_q = {'On lecture recordings': [
            'Wed Aug  2 18:26:40 2017', 'Testing1\n\nComplete.']}
        expected_a = {'On lecture recordings': [[
            'Thu Aug  3 18:59:12 2017', 'Testing2\n\nComplete.']]}
        self.assertEqual(
            actual_q, expected_q)
        self.assertEqual(
            actual_a, expected_a)
        print()

        print("UNIT2: 1 question, 2 answer")
        test_posts2 = [['Wed Aug  2 18:26:40 2017', 'On lecture recordings', 'Testing1\n\nComplete.'],
                       ['Thu Aug  3 18:59:12 2017',
                        'On lecture recordings', 'Testing2\n\nComplete.'],
                       ['Fri Aug  4 18:50:22 2017', 'On lecture recordings', 'Testing3\n\nComplete.']]
        actual_q2, actual_a2 = Parser.create_data_structures(test_posts2)
        expected_q2 = {'On lecture recordings': [
            'Wed Aug  2 18:26:40 2017', 'Testing1\n\nComplete.']}
        expected_a2 = {'On lecture recordings':
                       [['Thu Aug  3 18:59:12 2017', 'Testing2\n\nComplete.'],
                        ['Fri Aug  4 18:50:22 2017', 'Testing3\n\nComplete.']]}
        self.assertEqual(
            actual_q2, expected_q2)
        self.assertEqual(
            actual_a2, expected_a2)
        print()

        print("UNIT3: 2 question, 2 answer (1 each)")
        test_posts3 = [['Wed Aug  2 18:26:40 2017', 'On lecture recordings', 'Testing1\n\nComplete.'],
                       ['Thu Aug  3 18:59:12 2017',
                        'On lecture recordings', 'Testing2\n\nComplete.'],
                       ['Fri Aug  4 18:50:22 2017', 'I hate pointers',
                           'Testing3\n\nComplete.'],
                       ['Sun Aug  6 12:50:44 2017', 'I hate pointers', 'Testing4\n\nComplete.']]
        actual_q3, actual_a3 = Parser.create_data_structures(test_posts3)
        expected_q3 = {'On lecture recordings': [
            'Wed Aug  2 18:26:40 2017', 'Testing1\n\nComplete.'],
            'I hate pointers': ['Fri Aug  4 18:50:22 2017', 'Testing3\n\nComplete.']}
        expected_a3 = {'On lecture recordings':
                       [['Thu Aug  3 18:59:12 2017', 'Testing2\n\nComplete.']],
                       'I hate pointers': [['Sun Aug  6 12:50:44 2017', 'Testing4\n\nComplete.']]}
        self.assertEqual(
            actual_q3, expected_q3)
        self.assertEqual(
            actual_a3, expected_a3)
        print()

        print("UNIT4: 2 question, 2 answer (1 empty)")
        test_posts4 = [['Wed Aug  2 18:26:40 2017', 'On lecture recordings', 'Testing1\n\nComplete.'],
                       ['Thu Aug  3 18:59:12 2017',
                        'On lecture recordings', 'Testing2\n\nComplete.'],
                       ['Fri Aug  4 18:50:22 2017', 'I hate pointers',
                           'Testing3\n\nComplete.'],
                       ['Sun Aug  6 12:50:44 2017', 'On lecture recordings', 'Testing4\n\nComplete.']]
        actual_q4, actual_a4 = Parser.create_data_structures(test_posts4)
        expected_q4 = {'On lecture recordings': [
            'Wed Aug  2 18:26:40 2017', 'Testing1\n\nComplete.'],
            'I hate pointers': ['Fri Aug  4 18:50:22 2017', 'Testing3\n\nComplete.']}
        expected_a4 = {'On lecture recordings':
                       [['Thu Aug  3 18:59:12 2017', 'Testing2\n\nComplete.'], [
                           'Sun Aug  6 12:50:44 2017', 'Testing4\n\nComplete.']],
                       'I hate pointers': []}
        self.assertEqual(
            actual_q4, expected_q4)
        self.assertEqual(
            actual_a4, expected_a4)
        print()


if __name__ == '__main__':
    unittest.main()

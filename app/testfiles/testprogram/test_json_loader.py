import unittest
from json_loader import JsonLoader


class TestJson(unittest.TestCase):

    def test_json_storage(self):
        '''
        Tests to observer how the function successfully creates
        a JSON object when reading in a file with JSON data.
        '''

        file = 'testparsingfiles/testfile1.json'
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

        file = "testparsingfiles/TestFileExists.json"

        json = JsonLoader(file)
        actual1 = json.read_data()

        self.assertEqual(actual1, None)

    def test_file_json_readable(self):
        '''
        Tests to observer how the function handles non JSON readable
        data or invalid file formats for JSON extraction
        '''

        file = 'testparsingfiles/testfile.jpg'

        json = JsonLoader(file)
        actual1 = json.read_data()

        self.assertEqual(actual1, None)


if __name__ == '__main__':
    unittest.main()

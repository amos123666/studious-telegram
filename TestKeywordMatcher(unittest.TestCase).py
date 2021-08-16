import unittest

from app.domain.keywordmatcher import KeywordMatcher

class TestKeywordMatcher(unittest.TestCase):
    def test_keywordmatcher(self):
        # Please enter the keyword
        self.assertEqual((KeywordMatcher.getSuggestions(self,"It is a code"))[0], "How do I code well?")
        self.assertEqual((KeywordMatcher.getSuggestions(self, "we are a pointer"))[0], "How do I use pointers in C?")


if __name__ == '__main__':
    unittest

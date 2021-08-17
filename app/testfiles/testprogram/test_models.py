import unittest
from domain import UniversalEncoder, SentBERT


class TestModelEncoders(unittest.TestCase):

    def test_get_suggetions_Universal_Encoder(self):
        string = ''
        test_questions = 'app/parser/testparsingfiles/testfile2.json'
        encoder = UniversalEncoder(test_questions)
        suggestions1 = encoder.getSuggestions(string)

        self.assertEquals(suggestions1, None)

        string2 = 'plchatazpyiiihbkyisyamgfixbdiukplyeukfzeuoeyhzdlensohptbznnmggkwbkjyutpjjmvvz \
                   bozqdnyaefklodvpqvpqgboxtxulgixcejjuzxyqfwmfncjpirzerujaqrkhvrigmdhaylyzxayel \
                   kjepsevpqjgyctqzckmjrxuompdqyxpogpudjafupzlrqjxpkffqabxrohufolacipnrrrmkxovoyf \
                   jhjikhidwwehxwritzrztzpjovqyluzivpmbdhtlxazuqwdikadrnfhkaiugvcdbiczkzgxbaidbnj \
                   xqrwzozduwhwvneutchghmbjiyhqrvvvdazvuvceyavaystjqccjtnxadmnrlxahqsqjnlkovupwfd \
                   rwmiwziuiovagthhafaogavwcsrcpbglnlcrncsmuvfcoleirwpdbdijbsmugypucsjelemvgqlddbi \
                   vbqgajyjcxtgmwklbutzcnqcftluwslcabsgwhlagpegjz'

        encoder2 = UniversalEncoder(test_questions)
        suggestions2 = encoder2.getSuggestions(string)
        self.assertEquals(suggestions2, None)

    def test_get_suggetions_Sent_BERT(self):
        string = ''
        test_questions = 'app/parser/testparsingfiles/testfile2.json'
        encoder = SentBERT(test_questions)
        suggestions1 = encoder.getSuggestions(string)

        self.assertEquals(suggestions1, None)

        string2 = 'plchatazpyiiihbkyisyamgfixbdiukplyeukfzeuoeyhzdlensohptbznnmggkwbkjyutpjjmvvz \
                   bozqdnyaefklodvpqvpqgboxtxulgixcejjuzxyqfwmfncjpirzerujaqrkhvrigmdhaylyzxayel \
                   kjepsevpqjgyctqzckmjrxuompdqyxpogpudjafupzlrqjxpkffqabxrohufolacipnrrrmkxovoyf \
                   jhjikhidwwehxwritzrztzpjovqyluzivpmbdhtlxazuqwdikadrnfhkaiugvcdbiczkzgxbaidbnj \
                   xqrwzozduwhwvneutchghmbjiyhqrvvvdazvuvceyavaystjqccjtnxadmnrlxahqsqjnlkovupwfd \
                   rwmiwziuiovagthhafaogavwcsrcpbglnlcrncsmuvfcoleirwpdbdijbsmugypucsjelemvgqlddbi \
                   vbqgajyjcxtgmwklbutzcnqcftluwslcabsgwhlagpegjz'

        encoder2 = SentBERT(test_questions)
        suggestions2 = encoder2.getSuggestions(string)
        self.assertEquals(suggestions2, None)

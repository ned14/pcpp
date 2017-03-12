import unittest

class pcpp_doctests(unittest.TestCase):
    def runTest(self):
        import doctest, pcpp.preprocessor
        failurecount, testcount = doctest.testmod(pcpp.preprocessor)
        #self.assertGreater(testcount, 0)
        self.assertEqual(failurecount, 0)


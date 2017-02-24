import unittest

class pcpp_doctests(unittest.TestCase):
    def runTest(self):
        import doctest, pcpp.pcpp
        failurecount, testcount = doctest.testmod(pcpp.pcpp)
        #self.assertGreater(testcount, 0)
        self.assertEqual(failurecount, 0)


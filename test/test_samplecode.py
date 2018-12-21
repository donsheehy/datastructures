import unittest
from samplecode import SampleCode

class TestSampleCode(unittest.TestCase):
    def testsomething(self):
        s = SampleCode()
        self.assertTrue(s.dosomething())

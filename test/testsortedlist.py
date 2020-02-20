import unittest
from ds2.sortedlist import SortedList
from ds2.sortedlistsimple import SortedListSimple

class TestSortedListADT:
    def SortedList(self):
        raise NotImplementedError

    def testadd(self):
        pass

        
class TestSortedListSimple(unittest.TestCase, TestSortedListADT):
    SortedList = SortedListSimple

class TestSortedList(unittest.TestCase, TestSortedListADT):
    SortedList = SortedList


if __name__ == '__main__':
    unittest.main()

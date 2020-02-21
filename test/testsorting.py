import unittest
from ds2.dumbsort import dumbsort
from ds2.bubblesortsimple import bubblesort as bubblesortsimple
from ds2.bubblesort import bubblesort
from ds2.insertionsortsimple import insertionsort as insertionsortsimple
from ds2.insertionsort import insertionsort
from ds2.selectionsort import selectionsort
from ds2.mergesort import mergesort
from ds2.mergesort_iter import mergesort as mergesort_iter

class TestSorting:
    def testalreadysortedcase(self):
        L = [1,2,3]
        self.sort(L)
        self.assertEqual(L, [1,2,3])

    def testsmallexample(self):
        L = [4, 3, 1, 5, 9, 7, 6, 0, 2, 8]
        self.sort(L)
        self.assertEqual(L, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def testwithrepeats(self):
        L = [2,1,1,1,1,2,0,0,2]
        self.sort(L)
        self.assertEqual(L, [0, 0, 1, 1, 1, 1, 2, 2, 2])

    def testsortemptylist(self):
        L = []
        self.sort(L)
        # Mostly just checking that it didn't choke on [].
        self.assertEqual(L, [])


def test(sortingalgorithm):
    """Return a new testcase class for the given sorting algorithm.
    """
    class MySortingTest(unittest.TestCase, TestSorting):
        def sort(self, L):
            return sortingalgorithm(L)
    return MySortingTest

TestDumbSort = test(dumbsort)
TestBubbleSortSimple = test(bubblesortsimple)
TestBubbleSort = test(bubblesort)
TestSelectionSort = test(selectionsort)
TestInsertionSort = test(insertionsort)
TestInsertionSortSimple = test(insertionsortsimple)
TestMergeSort = test(mergesort)
TestMergeSortIter = test(mergesort_iter)

if __name__ == '__main__':
    unittest.main()

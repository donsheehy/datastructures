import unittest
from ds2.sorting import (dumbsort,
                        bubblesortsimple,
                        bubblesort,
                        insertionsortsimple,
                        insertionsort,
                        selectionsort,
                        mergesort,
                        mergesort_iter,
                        quicksort,
                        quicksort_long,
                        quicksorted,
                        heapsort,
                        )

class SortingTests:
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

    def testsortreversedlist(self):
        L = list(reversed(range(100)))
        self.sort(L)
        self.assertEqual(L, list(range(100)))

def _test(sortingalgorithm):
    """Return a new testcase class for the given sorting algorithm.
    """
    class MySortingTest(unittest.TestCase, SortingTests):
        def sort(self, L):
            return sortingalgorithm(L)
    return MySortingTest

TestDumbSort = _test(dumbsort)
TestBubbleSortSimple = _test(bubblesortsimple)
TestBubbleSort = _test(bubblesort)
TestSelectionSort = _test(selectionsort)
TestInsertionSort = _test(insertionsort)
TestInsertionSortSimple = _test(insertionsortsimple)
TestMergeSort = _test(mergesort)
TestMergeSortIter = _test(mergesort_iter)
TestQuickSort = _test(quicksort)
TestQuickSortLong = _test(quicksort_long)
TestHeapSort = _test(heapsort)

class TestQuickSorted(unittest.TestCase):
    def testsmallexample(self):
        L = [4, 3, 1, 5, 9, 7, 6, 0, 2, 8]
        S = quicksorted(L)
        self.assertEqual(S, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertFalse(S == L)

    def testlargerexample(self):
        L = list(range(100)) + list(reversed(range(100)))
        A = quicksorted(L)
        for i in range(200):
            self.assertEqual(i//2, A[i])

if __name__ == '__main__':
    unittest.main()

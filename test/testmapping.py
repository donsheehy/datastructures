import unittest
from ds2.mapping import Mapping
from ds2.listmappingsimple import ListMappingSimple
from ds2.listmapping import ListMapping
from ds2.listmapping_notDRY import ListMapping as ListMapping_notDRY
from ds2.hashmappingsimple import HashMappingSimple
from ds2.hashmapping import HashMapping
from ds2.hashmapping_notDRY import HashMapping as HashMapping_notDRY

class MappingTests:
    def Mapping(self):
        raise NotImplementedError

    def testput(self):
        M = self.Mapping()
        M.put(3, "three")
        M.put(1, "one")
        M.put(2, "two")

    def testgetandput(self):
        M = self.Mapping()
        M.put(3, "three")
        M.put(1, "one")
        self.assertEqual(M.get(1), "one")
        self.assertEqual(M.get(3), "three")
        self.assertEqual(M.get(1), "one")
        M.put(2, "two")
        self.assertEqual(M.get(2), "two")
        self.assertEqual(M.get(1), "one")

    def testgetraisesKeyError(self):
        M = self.Mapping()
        M.put(3, "three")
        M.put(1, "one")
        with self.assertRaises(KeyError):
            M.get(2)
        with self.assertRaises(KeyError):
            M.get("one")

    def testputoverwrites(self):
        M = self.Mapping()
        M.put(1, 1000)
        M.put(2, 'two')
        M.put(1, 'one')
        self.assertEqual(M.get(1), 'one')

class ExtendedMappingTests:
    def testlen(self):
        M = self.Mapping()
        for i in range(30):
            M.put(i, 2*i)
        self.assertEqual(len(M), 30)
        for i in range(40):
            M.put(i, i * 3)
        self.assertEqual(len(M), 40)

    def testcontains(self):
        M = self.Mapping()
        for i in range(10):
            M.put(i * 2, None)
        self.assertTrue(2 in M)
        self.assertTrue(4 in M)
        self.assertTrue(9 not in M)
        self.assertTrue(13 not in M)

    def testgetsetitem(self):
        M = self.Mapping()
        M[0] = 'test'
        M['test'] = 100
        self.assertEqual(M[0], 'test')
        self.assertEqual(M['test'], 100)

    def testiter(self):
        M = self.Mapping()
        keys = {'one', 'two', 'three', 1, 2, 3}
        for k in keys:
            M[k] = 100
        self.assertEqual(set(M), keys)

    def testvalues(self):
        M = self.Mapping()
        for i in range(10):
            M[2*i] = i + 30
        self.assertEqual(set(M.values()), set(range(30,40)))

    def testitems(self):
        M = self.Mapping()
        items = {(1, 'one'), (2,'two'), (3,'three')}
        for k, v in items:
            M[k] = v
        self.assertEqual(set(M.items()), items)

    def testmanyitems(self):
        M = self.Mapping()
        for i in range(1000):
            M[i] = 1
        self.assertEqual(len(M), 1000)

    def teststr(self):
        M = self.Mapping()
        M[1] = 2
        self.assertEqual(str(M), '{1 : 2}')

class TestListMappingSimple(unittest.TestCase, MappingTests):
    Mapping = ListMappingSimple

class TestListMapping(unittest.TestCase, MappingTests, ExtendedMappingTests):
    Mapping = ListMapping

class TestListMapping_notDRY(unittest.TestCase, MappingTests, ExtendedMappingTests):
    Mapping = ListMapping_notDRY

class TestHashMappingSimple(unittest.TestCase, MappingTests):
    Mapping = HashMappingSimple

class TestHashMapping(unittest.TestCase, MappingTests, ExtendedMappingTests):
    Mapping = HashMapping

class TestHashMapping_notDRY(unittest.TestCase, MappingTests, ExtendedMappingTests):
    Mapping = HashMapping_notDRY

class TestAbstractMapping(unittest.TestCase):
    """ These tests just check (and document) the methods that must
    be implemented by any class that extends `Mapping`.
    They are mostly here to exercise these code paths.
    """
    def testmustimplementget(self):
        M = Mapping()
        with self.assertRaises(NotImplementedError):
            M.get(1)

    def testmustimplementput(self):
        M = Mapping()
        with self.assertRaises(NotImplementedError):
            M.put(1, 2)

    def testmustimplementlen(self):
        M = Mapping()
        with self.assertRaises(NotImplementedError):
            len(M)

    def testmustimplement_entryiter(self):
        M = Mapping()
        with self.assertRaises(NotImplementedError):
            M._entryiter()


if __name__ == '__main__':
    unittest.main()

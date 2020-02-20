import unittest
from ds2.listmappingsimple import ListMappingSimple
from ds2.listmapping import ListMapping
from ds2.hashmappingsimple import HashMappingSimple
from ds2.hashmapping import HashMapping

class TestMapping:
    def Mapping(self):
        raise NotImplementedError

    def testget(self):
        pass

    def testput(self):
        pass


class TestListMappingSimple(unittest.TestCase, TestMapping):
    Mapping = ListMappingSimple

class TestListMapping(unittest.TestCase, TestMapping):
    Mapping = ListMapping

class TestHashMappingSimple(unittest.TestCase, TestMapping):
    Mapping = HashMappingSimple

class TestHashMapping(unittest.TestCase, TestMapping):
    Mapping = HashMapping

if __name__ == '__main__':
    unittest.main()

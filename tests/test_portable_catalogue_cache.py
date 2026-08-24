import unittest

from tools import portable_catalogue


class PortableCatalogueCacheTests(unittest.TestCase):
    def test_indexes_are_reused_within_process(self):
        portable_catalogue.indexes.cache_clear()
        first = portable_catalogue.indexes()
        second = portable_catalogue.indexes()
        self.assertIs(first, second)
        info = portable_catalogue.indexes.cache_info()
        self.assertEqual(info.misses, 1)
        self.assertGreaterEqual(info.hits, 1)

    def test_cached_indexes_cover_all_portable_layers(self):
        portable_catalogue.indexes.cache_clear()
        index = portable_catalogue.indexes()
        self.assertEqual(set(index), set(portable_catalogue.FILES))
        self.assertTrue(all(index[field] for field in portable_catalogue.FILES))


if __name__ == "__main__":
    unittest.main()

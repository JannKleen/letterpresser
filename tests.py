__author__ = 'Jann Kleen'

import unittest
import grid


class TestGrid(unittest.TestCase):
    def test_word(self):
        test_grid = grid.Grid([('a', 1), ('a', 1), ('a', 2)])
        self.assertEqual(test_grid.score_word('a'), 2)
        self.assertEqual(test_grid.score_word('aa'), 3)
        self.assertEqual(test_grid.score_word('aaa'), 4)
        self.assertEqual(test_grid.score_word('aba'), None)
        self.assertEqual(test_grid.score_word('aaaa'), None)

    def test_failing_init(self):
        with self.assertRaises(AssertionError):
             grid.Grid({'a': 1, 'b': 1, 'c': 2})

if __name__ == '__main__':
    unittest.main()

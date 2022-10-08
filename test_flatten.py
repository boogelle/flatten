
from flatten import flatten
import unittest


def f1():
    for val in range(10):
        yield val


class A:

    data = [[0], 1, 2, 3, [4, 5, 6, [7, 8, 9]]]

    def __eq__(self, other):
        return other == 'A'


class B(A):

    def __iter__(self):
        for val in self.data:
            yield val


class TestFlatten(unittest.TestCase):

    def test_00_empty_input(self):
        self.assertEqual(tuple(flatten(set())), tuple())
        self.assertEqual(tuple(flatten(list())), tuple())
        self.assertEqual(tuple(flatten(tuple())), tuple())

    def test_01_single_number(self):
        self.assertEqual(tuple(flatten(0)), (0,))
        self.assertEqual(tuple(flatten(1.)), (1.,))

    def test_02_single_string(self):
        self.assertEqual(tuple(flatten('qwe', flatten_strings=False)), ('qwe',))
        self.assertEqual(tuple(flatten('qwe', flatten_strings=True)), (*'qwe',))

    def test_10_shortest_sequences_of_numbers(self):
        self.assertEqual(tuple(flatten([0])), (0,))
        self.assertEqual(tuple(flatten((0,))), (0,))

    def test_11_shortest_sequences_of_strings(self):
        self.assertEqual(tuple(flatten(['qwe'], flatten_strings=False)), ('qwe',))
        self.assertEqual(tuple(flatten(('qwe',), flatten_strings=False)), ('qwe',))
        self.assertEqual(tuple(flatten(['qwe'], flatten_strings=True)), ('q', 'w', 'e'))
        self.assertEqual(tuple(flatten(('qwe',), flatten_strings=True)), ('q', 'w', 'e'))

    def test_13_shortest_dictionary(self):
        self.assertEqual(tuple(flatten({1: 'qwe'}, mapping_action='drop')), tuple())
        self.assertEqual(tuple(flatten({1: 'qwe'}, mapping_action='keep')), ({1: 'qwe'},))
        self.assertEqual(tuple(flatten({1: 'qwe'}, mapping_action='flatten_values')), ('qwe',))
        self.assertEqual(tuple(flatten({1: 'qwe'}, mapping_action='flatten_items')), (1, 'qwe'))
        self.assertEqual(tuple(flatten([{1: 'qwe'}], mapping_action='drop')), tuple())
        self.assertEqual(tuple(flatten([{1: 'qwe'}], mapping_action='keep')), ({1: 'qwe'},))
        self.assertEqual(tuple(flatten([{1: 'qwe'}], mapping_action='flatten_values')), ('qwe',))
        self.assertEqual(tuple(flatten([{1: 'qwe'}], mapping_action='flatten_items')), (1, 'qwe'))

    def test_20_sequence_of_numbers(self):
        self.assertEqual(tuple(flatten([0, 1, 2, [3, 4, 5, [6, 7, 8]], 9])), tuple(range(10)))
        self.assertEqual(tuple(flatten([0, 1, 2, (3, 4, 5, [6, 7, 8], 9)])), tuple(range(10)))
        self.assertEqual(tuple(flatten([[0], (1,), 2, 3, 4, 5, 6, 7, 8, 9])), tuple(range(10)))

    def test_21_sequence_of_strings(self):
        self.assertEqual(tuple(flatten(['qwe', ['r', 'ty']], flatten_strings=False)), ('qwe', 'r', 'ty'))
        self.assertEqual(tuple(flatten((('q',), 'wer', 't', 'y'), flatten_strings=False)), ('q', 'wer', 't', 'y'))
        self.assertEqual(tuple(flatten(['qwe', ['r', 'ty']], flatten_strings=True)), tuple('qwerty'))
        self.assertEqual(tuple(flatten((('q',), 'wer', 't', 'y'), flatten_strings=True)), tuple('qwerty'))

    def test_22_sequence_of_numbers_and_strings(self):
        self.assertEqual(
            tuple(flatten([0, [1, [2, 3]], 4, 5, 6, 7, 8, 9, 'qwe', ['r', 'ty']], flatten_strings=False)),
            (*range(10), 'qwe', 'r', 'ty'))
        self.assertEqual(
            tuple(flatten([0, [1, [2, 3]], 4, 5, 6, 7, 8, 9, 'qwe', ['r', 'ty']], flatten_strings=True)),
            (*range(10), *'qwerty'))

    def test_23_sequence_with_dictionaries(self):
        self.assertEqual(
            tuple(flatten([0, 1, 2, {3: [4, 5], 6: {7: 8}}, 9])),
            (0, 1, 2, 9))
        self.assertEqual(
            tuple(flatten([0, 1, 2, {3: [4, 5], 6: {7: 8}}, 9], mapping_action='keep')),
            (0, 1, 2, {3: [4, 5], 6: {7: 8}}, 9))
        self.assertEqual(
            tuple(flatten([0, 1, 2, {3: [4, 5], 6: {7: 8}}, 9], mapping_action='flatten_values')),
            (0, 1, 2, 4, 5, 8, 9))
        self.assertEqual(
            tuple(flatten([0, 1, 2, {3: [4, 5], 6: {7: 8}}, 9], mapping_action='flatten_items')),
            tuple(range(10)))
        self.assertEqual(
            tuple(flatten([{'qwe': 199, 'asd': 299, 'zxc': 399}], mapping_action='flatten_values')),
            (199, 299, 399))
        self.assertEqual(
            tuple(flatten([{'qwe': 199, 'asd': 299, 'zxc': 399}], mapping_action='flatten_items')),
            ('qwe', 199, 'asd', 299, 'zxc', 399))

    def test_30_sequences_with_generators(self):
        self.assertEqual(tuple(flatten(f1())), tuple(range(10)))
        self.assertEqual(tuple(flatten([*f1(), [10]])), tuple(range(11)))
        self.assertEqual(tuple(flatten([*f1(), ['qw', ['e']]], flatten_strings=True)), (*range(10), *'qwe'))

    def test_40_sequences_with_custom_types(self):
        self.assertEqual(tuple(flatten([A(), A()])), ('A', 'A'))
        self.assertEqual(tuple(flatten([A(), B()])), ('A', *range(10)))
        self.assertEqual(tuple(flatten([B(), B()])), (*range(10), *range(10)))


if __name__ == '__main__':
    unittest.main()

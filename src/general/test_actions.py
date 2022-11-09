import unittest
from .actions import (
    ascii_filter
)


class TestActions(unittest.TestCase):
    def test_ascii_filter(self):
        upper_limit = 127
        lower_limit = 0

        senteces = [
            f'this ✅ is a test📥',
            f'Test upper limit ->{chr(upper_limit)}',
            f'test lower {chr(lower_limit)}limit',
            f'test 1 above limit {chr(upper_limit+1)}',
            f'Test way over limit{chr(upper_limit+100)}'
        ]
        expected = [
            'this  is a test',
            'Test upper limit ->\x7f',
            'test lower \x00limit',
            'test 1 above limit ',
            'Test way over limit'
        ]

        data = [ascii_filter(sentence, lower_limit, upper_limit) for sentence in senteces]

        self.assertEqual(data, expected)
        
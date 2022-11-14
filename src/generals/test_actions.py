import json
import unittest
from .settings import Settings
from .constants import SCAM_SAMPLES
from .actions import (
    ascii_filter,
    find_next_sample,
    total_samples,
)


class TestActions(unittest.TestCase):
    def setUp(self) -> None:
        self.scam_samples = '../samples'

    def test_ascii_filter(self):
        upper_limit = 127
        lower_limit = 0

        senteces = [
            'this ✅ is a test📥',
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

        data = [
            ascii_filter(sentence, lower_limit, upper_limit)
            for sentence in senteces
        ]

        self.assertEqual(data, expected)

    def test_find_next_sample(self):
        next = total_samples(SCAM_SAMPLES) + 1
        file = f"{next}.txt"
        self.assertEqual(find_next_sample(self.scam_samples), file)


class TestSettings(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_settings = {
            'key1': 'value1',
            'key2': 'value2',
        }
        self.settings = Settings('../.testsettings.json')
        with open(self.settings.settings_path, mode='w') as f:
            json.dump(self.initial_settings, f)

    def tearDown(self) -> None:
        # Reset settings
        with open(self.settings.settings_path, mode='w') as f:
            json.dump(self.initial_settings, f)

    def test_load_all(self):
        self.assertEqual(self.initial_settings, self.settings.all)

    def test_get(self):
        self.assertEqual(
            self.initial_settings['key1'],
            self.settings.get('key1')
        )

    def test_set(self):
        key = 'key1'
        value = 'test1'
        self.settings.set(key, value)
        self.assertEqual(self.settings.get(key), value)

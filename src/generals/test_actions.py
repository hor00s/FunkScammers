import os
import json
import unittest
from .settings import Settings
from .constants import SCAM_SAMPLES
from .actions import (
    increment_config,
    ascii_filter,
    load_samples,
    is_imported,
    reset_logs,
    read_file,
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

    def test_load_samples(self):
        for i in load_samples(SCAM_SAMPLES):
            self.assertIsInstance(i, str)

    def test_is_imported(self):
        self.assertTrue(is_imported('json'))
        self.assertFalse(is_imported('spacy'))

    def test_read_file(self):
        self.assertIsInstance(read_file(SCAM_SAMPLES), str)


class TestSettings(unittest.TestCase):
    def setUp(self) -> None:
        self.initial_settings = {
            'key1': 'value1',
            'key2': 'value2',
            'total_runs': '0',
            'reset_logs_after': '5'
        }

        self.settings = Settings(
            '../.testsettings.json',
            **self.initial_settings
        )
        self.settings.init()
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

    def test_delete_logs(self):
        with open('test_logs.txt', mode='w') as f: f.write('tes')

        config_name = 'total_runs'
        test_logs = 'test_logs.txt'

        for i in range(0, 6):
            runs = int(self.settings.get(config_name))
            self.assertEqual(runs, i)

            self.assertEqual(i, runs)
            reset_logs(test_logs, self.settings)
            increment_config(self.settings, config_name)

            self.assertTrue(os.path.exists(test_logs))

        increment_config(self.settings, config_name)

        __builtins__['input'] = lambda _: "y"
        reset_logs(test_logs, self.settings)

        with open(test_logs, mode='r') as f:
            self.assertEqual(f.read(), '')

    def test_checkout(self):
        new_key = 'new_key'
        self.settings.conf[new_key] = 'new_val'
        self.settings._checkout()
        self.assertIn(new_key, self.settings.all)

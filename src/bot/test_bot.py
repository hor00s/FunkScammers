import unittest
from .bot import Bot


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.usernm = 'username'
        self.passwd = 'password'
        self.bot = Bot(self.usernm, self.passwd)

    def test_properties(self):
        self.assertEqual(self.usernm, self.bot.name)
        self.assertEqual(self.passwd, self.bot.password)

    def test_is_sus(self):
        max_num = 0.7
        total_matches = 1
        data = [
            'This text is weird',
            'A boy with a red shirt',
            'This text is dangerous',
        ]

        # True case
        text = 'This text is sus'
        is_sus = self.bot.is_sus(text, data, max_num, total_matches)
        self.assertTrue(is_sus, msg="The bot can be a little un-predicted!")

        # False case
        text = 'A completely unrelated text document'
        is_sus = self.bot.is_sus(text, data, max_num, total_matches)
        self.assertFalse(is_sus, msg="The bot can be a little un-predicted!")

    def test_get_success_percentage(self):
        v0 = self.bot.get_success_percentage(0, 10)
        self.assertEqual(v0, 100.00)

        v1 = self.bot.get_success_percentage(10, 10)
        self.assertEqual(v1, 50.00)

        v3 = self.bot.get_success_percentage(4, 12)
        self.assertEqual(v3, 75.00)

        v4 = self.bot.get_success_percentage(24, 8)
        self.assertEqual(v4, 25.00)

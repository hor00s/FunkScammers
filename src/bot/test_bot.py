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
        data = [
            'This text is weird',
            'A boy with a red shirt',
            'This text is dangerous',
        ]

        # True case
        text = 'This text is sus'
        is_sus = self.bot.is_sus(text, data, max_num)
        self.assertTrue(is_sus)

        # False case
        text = 'A completely unrelated text document'
        is_sus = self.bot.is_sus(text, data, max_num)
        self.assertFalse(is_sus)

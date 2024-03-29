import unittest
from .bot import Bot


class TestBot(unittest.TestCase):
    def setUp(self) -> None:
        self.usernm = 'test_db'
        self.passwd = 'password'
        self.bot = Bot(self.usernm, self.passwd)

    def test_properties(self) -> None:
        self.assertEqual(self.usernm, self.bot.name)
        self.assertEqual(self.passwd, self.bot.password)

    def test_aleady_replied(self) -> None:
        comment_id = 'fsart'
        not_replied = self.bot.already_replied(
            'te',
        )

        replied = self.bot.already_replied(
            comment_id,
        )

        self.assertFalse(not_replied, msg="The bot shouldn't reply here")
        self.assertTrue(replied, msg="The bot should reply here")

    def test_is_sus(self) -> None:
        max_num = 0.7
        total_matches = 1
        data = [
            'This text is weird',
            'A boy with a red shirt',
            'This text is dangerous',
        ]

        # True case
        text = 'This text is sus'
        is_sus = self.bot.is_sus(text, data, max_num, total_matches, [])
        self.assertTrue(is_sus, msg="The bot can be a little un-predicted!")

        # False case
        text = 'A completely unrelated text document'
        is_sus = self.bot.is_sus(text, data, max_num, total_matches, [])
        self.assertFalse(is_sus, msg="The bot can be a little un-predicted!")

    def test_get_success_percentage(self) -> None:
        v0 = self.bot.get_success_percentage(0, 10)
        self.assertEqual(v0, 100.00)

        v1 = self.bot.get_success_percentage(10, 10)
        self.assertEqual(v1, 50.00)

        v3 = self.bot.get_success_percentage(4, 12)
        self.assertEqual(v3, 75.00)

        v4 = self.bot.get_success_percentage(24, 8)
        self.assertEqual(v4, 25.00)

    def test_parse(self) -> None:
        text = """

        This is a text that

        contains new lines,  unneccesary spaces
            and some indentation.

        we will also add some empty lines

        /s
        """
        expected = ['this', 'is', 'a', 'text', 'that', 'contains', 'new', 'lines', 'unneccesary', 'spaces', 'and', 'some', 'indentation', 'we', 'will', 'also', 'add', 'some', 'empty', 'lines', '/s']  # noqa
        self.assertEqual(list(self.bot._parse_text(text)), expected)

    def test_abort(self) -> None:
        abort_chars = ['/s', '/j']
        text = """

        This is a text that

        contains new lines,  unneccesary spaces
            and some indentation.

        we will also add some empty lines

        /s
        """

        self.assertTrue(self.bot.text_is_s(text, abort_chars))

        text = """

        This is a text that

        contains new lines,  unneccesary spaces
            and some indentation.

        we will also add some empty lines

        """
        self.assertFalse(self.bot.text_is_s(text, abort_chars))

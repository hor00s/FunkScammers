import os
import unittest
from .model import Model
from sqlite3 import OperationalError


class TestModel(unittest.TestCase):
    def setUp(self) -> None:
        self.table = {
            'user': 'TEXT',
            'age': 'INTEGER',
            'reply_id': 'TEXT'
            # 'id': 'PRIMARY KEY' Remember `id` is inserted by default
        }

        self.model = Model('test_db', **self.table)

    def test_create(self) -> None:
        self.model.create_table()
        self.assertTrue(os.path.exists(self.model.name + '.sqlite'))

    def test_insert(self) -> None:
        self.model.insert(user='john', age=25)
        data = self.model.fetch_all()
        self.assertGreater(len(data), 0)
        self.assertEqual(len(self.model.fetch_last()), 4)

    def test_edit(self) -> None:
        self.model.insert(user='john', age=25)
        new_name = 'anna'
        self.model.edit(f"user='{new_name}'", "user='john'")
        data = self.model.fetch_all()
        self.assertEqual(data[0][0], new_name)

    def test_fetch_last(self) -> None:
        last_by = self.model.fetch_last('id')
        all_data = self.model.fetch_last()
        self.assertIsInstance(all_data, tuple)
        self.assertEqual(last_by, all_data[3])

    def test_insert_one(self) -> None:
        name = 'Elvis'
        self.model.insert(user=name)
        insertion = self.model.fetch_last('user')
        self.assertEqual(name, insertion)

    def test_wrong_cols(self) -> None:
        insert = self.model.insert
        with self.assertRaises(OperationalError):
            insert(non_existing='something')

    def test_filter(self) -> None:
        self.model.insert(user='test', age=5, reply_id='fsart')

        expected = self.model.fetch_last('reply_id')
        self.assertEqual(expected, 'fsart')

import os
import io
import unittest
import unittest.mock
from logger import Logger, Config


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger(1)

    def tearDown(self) -> None:
        self.logger = Logger(1)

    def test_invalid_instance(self):
        with self.assertRaises(ValueError, msg='An instance with level=0 is created'):
            Logger(0)

        with self.assertRaises(ValueError, msg='An instance with level=6 is created'):
            Logger(6)

        logger = Logger(2)
        with self.assertRaises(ValueError, msg='A settings instance changed level above limit after creation'):  # noqa
            logger.settings.level = 6

        logger = Logger(2)
        with self.assertRaises(ValueError, msg='A settings instance changed level above limit after creation'):  # noqa
            logger.settings.level = 0

    def test_instance_counter(self):
        Config._INSTANCE = 0
        l1 = Logger()
        self.assertEqual(l1.settings._INSTANCE, 1, msg="First instance counter is wrong")
        l2 = Logger()
        self.assertEqual(l2.settings._INSTANCE, 2, msg="Second instance counter is wrong")

        self.assertEqual(l1.settings._INSTANCE, 1, msg="Repeated instance counter is wrong")

    def test_update_settings(self):
        self.logger.settings.update(success=4)
        self.assertEqual(self.logger.settings['success'], 4)

        with self.assertRaises(TypeError, msg="self.logger object is directly assignable"):
            self.logger.settings['success'] = 4

        with self.assertRaises(ValueError, msg="not existing key passed into self.settings"):
            self.logger.settings.update(not_exists=4)

        with self.assertRaises(TypeError, msg="String passed as value in self.settings"):
            self.logger.settings.update(success='4')

        with self.assertRaises(ValueError, msg='0 Passed as valid key in self.settings'):
            self.logger.settings.update(success=0)

        with self.assertRaises(ValueError, msg="Above the allowed limit passed as valid key in self.settings"):  # noqa
            self.logger.settings.update(success=6)

        with self.assertRaises(AttributeError, msg="self.settings is overwritable (`=`)"):
            self.logger.settings.settings = 'fsaf'

        self.logger.settings.update(success=2, info=1)
        self.assertEqual(self.logger.settings['success'], 2, msg='Error in updating 2 values at once at `success`')  # noqa
        self.assertEqual(self.logger.settings['info'], 1, msg='Error in updating 2 values at once at `info`')  # noqa

    def test_get_settings(self):
        with self.assertRaises(AttributeError, msg="self.settings is overwritable (`=`) instead of read-only"):  # noqa
            self.logger.settings = 'fsaf'

    def test_get_setting(self):
        self.assertEqual(self.logger.settings.get('info'), 3, msg="settings.get() returns value from wrong key or the value has changed")  # noqa
        with self.assertRaises(KeyError):
            self.logger.settings.get('not_existing')

    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_success_msg(self, mock_stdout):
        msg = "anythong"

        self.logger.settings.level = 5
        self.logger.success(msg)
        self.assertFalse(mock_stdout.getvalue())

        self.logger.info(msg)
        self.assertFalse(mock_stdout.getvalue())

        self.logger.settings.level = 1
        self.logger.success(msg)
        self.assertTrue(mock_stdout.getvalue())

        self.logger.info(msg)
        self.assertTrue(mock_stdout.getvalue())

    def test_iter_next(self):
        total0 = 0
        for _ in self.logger.settings:
            total0 += 1

        total1 = 0
        for _ in self.logger.settings:
            total1 += 1

        self.assertEqual(total0, total0, msg="There is something wrong with Config.__iter__ and Config.__next__. Maybe the index (self._iter) is not refreshing correctly")  # noqa

    def test_log_to_file(self):
        msg = 'This should be written in the file'
        file = 'test.txt'
        logger = Logger(1, file)
        logger.info(msg)

        self.assertTrue(os.path.exists(file))
        with open(file, mode='r') as f:
            self.assertEqual(f"[INFO]: {msg}", f.read()[:-1])  # Slice to remove '\n' from the file
        os.remove(file)

# TODO: Test the effect of the metaclass

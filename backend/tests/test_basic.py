import unittest

from django.test import TestCase

from utils.register_params_check import register_params_check


class BasicTestCase(TestCase):

    def test_register_params_check(self):
        self.assertEqual(register_params_check({}), ("ok", True))


if __name__ == "__main__":
    unittest.main()

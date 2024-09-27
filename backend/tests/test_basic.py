import unittest

from django.test import TestCase

from utils.register_params_check import register_params_check, validate_username, validate_password, validate_mobile, validate_url


class TestRegisterParamsCheck(TestCase):
    """
    TODO: 在这里补充注册相关测试用例
    """

    def test_invalid_username(self):
        # missing username
        self.assertEqual(register_params_check({}), ('username', False))

        # invalid usernames
        self.assertEqual(register_params_check({'username': 123}), ('username', False))
        self.assertEqual(register_params_check({'username': 'a'}), ('username', False))
        self.assertEqual(register_params_check({'username': 'a1'}), ('username', False))
        self.assertEqual(register_params_check(
            {'username': 'aaaaaa1222222222'}), ('username', False))
        self.assertEqual(register_params_check({'username': 'abcdefg'}), ('username', False))
        self.assertEqual(register_params_check({'username': '1234567'}), ('username', False))
        self.assertEqual(register_params_check({'username': '1234abcd'}), ('username', False))

    def test_invalid_password(self):
        # missing password
        self.assertEqual(register_params_check({'username': 'abcd1234'}), ('password', False))

        # invalid passwords
        self.assertEqual(register_params_check({'username': 'abcd1234', 'password':'aA1.'}), ('password', False))
        # self.assertEqual(register_params_check({'username': 'abcd1234', '':''}))
    
    def test_username(self):
        # invalid usernames
        self.assertEqual(validate_username(''), False)
        self.assertEqual(validate_username(123), False)
        self.assertEqual(validate_username('a'), False)
        self.assertEqual(validate_username('a1'), False)
        self.assertEqual(validate_username('aaaaaa1222222222'), False)
        self.assertEqual(validate_username('abcdefg'), False)
        self.assertEqual(validate_username('1234567'), False)
        self.assertEqual(validate_username('1234abcd'), False)

        # valid usernames
        self.assertEqual(validate_username('abc123'), True)



if __name__ == "__main__":
    unittest.main()

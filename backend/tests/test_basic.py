import unittest

from django.test import TestCase

from utils.register_params_check import (register_params_check,
                                         validate_mobile, validate_password,
                                         validate_url, validate_username)


class TestRegisterParamsCheck(TestCase):
    # test each individual step used in register_params_check
    def test_username(self):
        # invalid usernames
        self.assertFalse(validate_username(''))
        self.assertFalse(validate_username(123))
        self.assertFalse(validate_username('a'))
        self.assertFalse(validate_username('a1'))
        self.assertFalse(validate_username('aaaaaa1222222222'))
        self.assertFalse(validate_username('abcdefg'))
        self.assertFalse(validate_username('1234567'))
        self.assertFalse(validate_username('1234abcd'))

        # valid usernames
        self.assertTrue(validate_username('abc123'))
        self.assertTrue(validate_username('a1234'))
        self.assertTrue(validate_username('abcdeg9'))

    def test_password(self):
        # invalid passwords
        self.assertFalse(validate_password('aA1-'))
        self.assertFalse(validate_password('abcd1234-'))
        self.assertFalse(validate_password('ABCD1234-'))
        self.assertFalse(validate_password('ABcd-_*^'))
        self.assertFalse(validate_password('ABcd1234'))
        self.assertFalse(validate_password('Abcd1234-_*^sjdflkasjdfalkdf'))
        self.assertFalse(validate_password('bcAD14.=+'))

        # valid passwords
        self.assertTrue(validate_password('abcdEFG123_-'))
        self.assertTrue(validate_password('1234_*^-zxV'))

    def test_mobile(self):
        # invalid mobile numbers
        self.assertFalse(validate_mobile('12.123456789012'))
        self.assertFalse(validate_mobile('+12123456789012'))
        self.assertFalse(validate_mobile('+12.12345678901'))
        self.assertFalse(validate_mobile('+1.123456789012'))
        self.assertFalse(validate_mobile('+.123456789012'))
        self.assertFalse(validate_mobile('+12.'))
        self.assertFalse(validate_mobile('+123.123456789012'))
        self.assertFalse(validate_mobile('+123.123456789012'))
        self.assertFalse(validate_mobile('12+312.3456789012'))

        # some valid ones
        self.assertTrue(validate_mobile('+00.000000000000'))
        self.assertTrue(validate_mobile('+31.123456789012'))

    def test_url(self):
        # some invalid URLs
        self.assertFalse(validate_url('asdf.com'))
        self.assertFalse(validate_url('https://asf.123'))
        self.assertFalse(validate_url('https://asf'))
        self.assertFalse(validate_url('https://'))
        self.assertFalse(validate_url('http://asf..com'))
        self.assertFalse(validate_url('https://a-sf.-com'))
        self.assertFalse(validate_url('https://a-sf.com-'))
        self.assertFalse(validate_url('https://A-s(f.com'))

        # some valid  URLs
        self.assertTrue(validate_url('http://www.google.com'))
        self.assertTrue(validate_url('http://123.9A-Zfa9sfc.c123'))
        self.assertTrue(validate_url('https://a.b'))

    def test_register_params_check(self):
        params = {'username': 'user123', 'password': 'abCD1234-_*^', 'nickname': 'nick',
                  'mobile': '+12.123456789012', 'url': 'https://www.google.com'}

        self.assertEqual(register_params_check(params), ('ok', True))
        self.assertEqual(params['magic_number'], 0)

        # test username
        bad_username_params = {**params}
        del bad_username_params['username']
        self.assertEqual(register_params_check(bad_username_params), ('username', False))

        bad_username_params['username'] = 123
        self.assertEqual(register_params_check(bad_username_params), ('username', False))

        # test password
        bad_password_params = {**params}
        del bad_password_params['password']
        self.assertEqual(register_params_check(bad_password_params), ('password', False))

        bad_password_params['password'] = None
        self.assertEqual(register_params_check(bad_password_params), ('password', False))

        # test nickname
        bad_nick_params = {**params}
        del bad_nick_params['nickname']
        self.assertEqual(register_params_check(bad_nick_params), ('nickname', False))

        # test mobile
        bad_mobile_params = {**params}
        del bad_mobile_params['mobile']
        self.assertEqual(register_params_check(bad_mobile_params), ('mobile', False))

        bad_mobile_params['mobile'] = 13131
        self.assertEqual(register_params_check(bad_mobile_params), ('mobile', False))

        # test url
        bad_url_params = {**params}
        del bad_url_params['url']
        self.assertEqual(register_params_check(bad_url_params), ('url', False))

        # test magic number
        params['magic_number'] = -1
        self.assertEqual(register_params_check(params), ('magic_number', False))
        params['magic_number'] = 123132
        self.assertEqual(register_params_check(params), ('ok', True))


if __name__ == "__main__":
    unittest.main()

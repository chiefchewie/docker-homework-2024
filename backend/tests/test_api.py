import unittest

from django.test import Client, TestCase
from django.urls import reverse

from user import views as user_views
from user.models import User
from utils.jwt import encrypt_password


class APITestCase(TestCase):

    def setUp(self):
        user = User(username="testuser", password=encrypt_password(str("testuser")),
                    nickname="test", mobile="+86.123456789012", magic_number=0, url="https://baidu.com")
        user.save()
        self.client = Client()

    def test_login(self):
        """
        使用错误的信息进行登录，检查返回值为失败
        """
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.patch(
            '/api/v1/login',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], "Invalid credentials")
        self.assertEqual(response.status_code, 401)

        """
        使用正确的信息进行登录，检查返回值为成功
        """
        data = {"username": "testuser", "password": "testuser"}
        response = self.client.patch(
            '/api/v1/login',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", json_data)
        self.assertIn("userId", json_data)
        self.assertIn("username", json_data)
        self.assertIn("nickname", json_data)

        jwt = json_data['jwt']

        """
        进行登出，检查返回值为成功
        """
        auth_header = {'Authorization': jwt}
        response = self.client.post(
            reverse(user_views.logout),
            headers=auth_header,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], 'ok')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        """
        Example: 使用错误信息进行注册，检查返回值为失败
        """
        data = {"username": "123", "password": "21321"}
        response = self.client.post(
            reverse(user_views.register_user),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], 'Invalid arguments: username')
        self.assertEqual(response.status_code, 400)

        """
        使用正确的信息进行注册，检查返回值为成功
        """
        data = {"username": "user12344", "password": "abCD12-_",
                "nickname": "nick", "mobile": "+00.000000000000", "url": "https://a.b"}
        response = self.client.post(
            reverse(user_views.register_user),
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], 'ok')
        self.assertEqual(response.status_code, 200)

        """
        使用正确注册信息进行登录，检查返回值为成功
        """
        data = {"username": "user12344", "password": "abCD12-_"}
        response = self.client.patch(
            '/api/v1/login',
            data=data,
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", json_data)
        self.assertIn("userId", json_data)
        self.assertIn("username", json_data)
        self.assertIn("nickname", json_data)

    def test_logout(self):
        """
        未登录直接登出
        """
        response = self.client.post(
            reverse(user_views.logout),
            content_type="application/json"
        )
        json_data = response.json()
        self.assertEqual(json_data['message'], 'User must be authorized.')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()

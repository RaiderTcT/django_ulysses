# -*- coding: utf-8 -*-
# @Date    : 2018-11-21 20:12:24
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
from django.test import TestCase, Client
from django.contrib.auth.models import User
from ..models import Topic, Post
from django.conf import settings


class ClientTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        SimpleTestCase and its subclasses (e.g. TestCase, …) rely on setUpClass() and tearDownClass()
        to perform some class-wide initialization (e.g. overriding settings).
        If you need to override those methods, don’t forget to call the super implementation:
        """
        super().setUpClass()
        User.objects.create_user('Admin', 'admin@qq.com', 'admin12345')
        cls.login = {'username': 'Admin', 'password': 'admin12345'}
        cls.client = Client()

    # def setUp(self):
    #     User.objects.create_user('Admin', 'admin@qq.com', 'admin12345')
    #     self.login = {'username': 'Admin', 'password': 'admin12345'}
    #     self.client = Client()

    def test_home_page_en(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Weicome to my site' in response.content.decode('utf-8'))

    def test_home_page_zh(self):
        response = self.client.get('/zh-hans/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('欢迎来到我的网站' in response.content.decode('utf-8'))

    def test_login(self):
        """测试登录页面"""
        response = self.client.post('/en/users/login/', **self.login)
        self.assertEqual(response.status_code, 200)
        # self.assertTrue(self.client.login(**self.login))

    def test_post_topic(self):
        """登录后，创建topic再读取"""
        self.client.login(**self.login)
        self.client.post('/en/new_topic/', {'text': '红尘多可笑，痴情最无聊'})
        topic = Topic.objects.get(text='红尘多可笑，痴情最无聊')
        self.assertIsNotNone(topic)
        response = self.client.get(f'/en/topic/{topic.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['topic'], topic)

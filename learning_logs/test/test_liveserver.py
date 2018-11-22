# -*- coding: utf-8 -*-
# @Date    : 2018-11-22 13:54:50
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
import re
import time


class MySeleniumTests(LiveServerTestCase):
    """ 定位UI元素
        ID = "id"
        XPATH = "xpath"
        LINK_TEXT = "link text"
        PARTIAL_LINK_TEXT = "partial link text"
        NAME = "name"
        TAG_NAME = "tag name"
        CLASS_NAME = "class name"
        CSS_SELECTOR = "css selector"
    """
    # host = 'localhost'
    # port = 0

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = ChromeOptions()
        options.add_argument('headless')
        cls.selenium = Chrome(options=options)
        # 设置粘滞超时以隐式等待找到元素或完成命令。
        cls.selenium.implicitly_wait(5)
        User.objects.create_user('Admin', 'admin@qq.com', 'admin12345')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_home_page(self):
        """
        测试打开主页
        cls.live_server_url: 'http://%s:%s' % (cls.host, cls.server_thread.port)
        """
        self.selenium.get(f"{self.live_server_url}/en/")
        self.assertTrue(re.search('Weicome\s+to\s+my\s+site', self.selenium.page_source))

    def test_login(self):
        timeout = 5
        self.selenium.get(f"{self.live_server_url}/en/")
        self.selenium.find_element_by_link_text('Login').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name('username'))
        self.selenium.find_element_by_name('username').clear()
        self.selenium.find_element_by_name('username').send_keys('Admin')
        self.selenium.find_element_by_name('password').clear()
        self.selenium.find_element_by_name('password').send_keys('admin12345')
        self.selenium.find_element_by_name('submit').click()
        # time.sleep(2)
        element = WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_id('navbarDropdown'))
        self.assertTrue(re.search('Weicome\s+to\s+my\s+site', self.selenium.page_source))
        # self.selenium.find_element_by_id('navbarDropdown').click()
        element.click()
        # time.sleep(2)
        element = WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_name('profile'))
        element.click()
        # self.selenium.find_element_by_name('profile').click()
        self.assertTrue(re.search('<h2>Admin</h2>', self.selenium.page_source))

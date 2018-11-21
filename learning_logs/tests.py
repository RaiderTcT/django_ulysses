from django.test import TestCase
from learning_logs.models import Topic, Post, User
import time
# Create your tests here.


class TopicTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='TestUser', email='test@qq.com', password='password')
        Topic.objects.create(owner=self.user, text='topic test 1')
        Topic.objects.create(owner=self.user, text='topic test 2')

    def test_topic_user(self):
        topic_1 = Topic.objects.get(text='topic test 1')
        topic_2 = Topic.objects.get(text='topic test 2')
        self.assertEqual(topic_1.owner, self.user)
        self.assertEqual(topic_2.owner, self.user)


class PostTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='PostUser', email='test@qq.com', password='password')
        user = User.objects.create_user(
            username='TopicUser', email='test@qq.com', password='password')
        topic = Topic.objects.create(owner=user, text='topic test 1')
        Post.objects.create(id=1, topic=topic, owner=self.user, text='# post test')

    def test_post_owner(self):
        post = Post.objects.get(id=1)
        self.assertEqual(post.owner, self.user)

    def test_post_html_content(self):
        post = Post.objects.get(id=1)
        post.text = '## post test'
        post.save()
        self.assertEqual(post.html_content, '<h2>post test</h2>')

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save
from markdown import markdown
from mdeditor.fields import MDTextField
from django.urls import reverse
# Create your models here.


class Topic(models.Model):
    """主题"""
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='the owner of this topic')

    class Meta:
        app_label = 'learning_logs'

    def get_absolute_url(self):
        return reverse('learning_logs:my_topics')

    def __str__(self):
        return self.text


class Post(models.Model):
    """同一Topic下的多篇文章"""
    # many to one relationship
    id = models.AutoField(primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='the related topic')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='the owner of the post')
    # text = models.TextField('post content')
    text = MDTextField()
    html_content = models.TextField('html content', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now=True)

    # Model metadata is “anything that’s not a field”, such as ordering options (ordering),
    #  database table name (db_table),
    # or human-readable singular and plural names (verbose_name and verbose_name_plural).
    # None are required, and adding class Meta to a model is completely optional.
    class Meta:
        verbose_name_plural = 'posts'
        app_label = 'learning_logs'

    def get_absolute_url(self):
        return reverse('learning_logs:topic', args=(self.topic.id,))

    def __str__(self):
        return self.text[:50] + '...'


class TestModel(models.Model):
    topic = models.ManyToManyField(Topic)
    headline = models.CharField(max_length=255)

    def __str__(self):
        return self.headline


# 只提交Markdown源文本，在服务器上进行转换
# instance 正要被保存的Post对象实例
# update_fields 要更新的字段
@receiver(pre_save, sender=Post)
def md_trans(sender, update_fields=None, instance=None, **kwargs):
    """在post文本提交时，进行markdown转html"""
    instance.html_content = markdown(instance.text, extensions=['markdown.extensions.extra', ])
    update_fields = ['html_content', ]

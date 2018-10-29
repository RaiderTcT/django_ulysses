from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Topic(models.Model):
    """主题"""
    id = models.IntegerField(auto_created=True, primary_key=True)
    text = models.CharField(max_length=20)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE ,verbose_name='the owner of this topic')

    def __str__(self):
        return self.text

class Post(models.Model):
    """同一Topic下的多篇文章"""
    # many to one relationship
    id = models.IntegerField(auto_created=True, primary_key=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name='the related topic')
    text = models.TextField('post content')
    date_added = models.DateTimeField(auto_now_add=True)
    date_edit = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'posts'

    def __str__(self):
        return  self.text[:50] + '...'
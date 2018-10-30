from django.forms import Form, ModelForm, Textarea, CharField
from .models import Topic, Post



class TopicForm(ModelForm):
    """Topic表单"""
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ""}


class PostForm(ModelForm):
    """Post表单"""
    class Meta:
        model = Post # 模型
        fields = ['text']   # 表单字段
        labels = {'text': ""} # verbose name
        widgets = {
            'text': Textarea(attrs={'cols': 80}),
        }
from django.forms import Form, ModelForm, Textarea, CharField
from .models import Topic, Post



class TopicForm(Form):
    """Topic表单"""
    topic_name = CharField(label='主题:', max_length=20)

class PostForm(ModelForm):
    """Post表单"""
    class Meta:
        model = Post # 模型
        fields = ['text']   # 表单字段
        labels = {'text': ""} # verbose name
        widgets = {
            'text': Textarea(attrs={'cols': 80}),
        }
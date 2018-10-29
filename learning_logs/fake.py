"""用于生成虚拟topic 和 post"""
from random import randint
from faker import Faker
from .models import Topic, Post

def topics(count=100):
    print(f"count={count}")
    fake = Faker()
    i = 0
    while i < count:
        t = Topic(id=i, text=fake.text())
        t.save()
        i = i + 1

def posts(count=100):
    fake = Faker()
    i = 0
    topic_count = Topic.objects.count()
    for i in range(count):
        # 在随机Topic下生成Post
        count_1 = randint(0, topic_count-1)
        print(f"topic_id:{count_1}")
        t = Topic.objects.get(id=count_1)
        print(t)
        p = Post(id=i, text=fake.text(), topic=t)
        p.save()

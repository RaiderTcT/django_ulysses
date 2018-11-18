from django.contrib.sitemaps import Sitemap
from learning_logs.models import Topic, Post

class TopicSitemap(Sitemap):

    # the change frequency of every object returned by items().
    changefreq = 'daily'
    priority = 0.5
    i18n = True
    # 必须添加 提供对象列表。
    # 框架并不关心对象的类型，唯一关心的是这些对象。
    def items(self):
        return Topic.objects.all().filter()
    # 对象的最后修改日期
    def lastmod(self, obj):
        return obj.date_added

    # 给定对象的绝对URL。 绝对URL不包含协议名称和域名。
    # 如果没有提供 location , 框架将会在每个 items() 返回的对象上调用 get_absolute_url() 方法
    def location(self, obj):
        return f'/topic/{obj.id}'

class PostSitemap(Sitemap):

    changefreq = 'daily'
    priority = 0.5

    def items(self):
        return Post.objects.all().filter()

    def lastmod(self, obj):
        return obj.date_edit

    def location(self, obj):
        return f'/topic/{obj.id}'
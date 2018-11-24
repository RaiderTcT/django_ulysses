# -*- coding: utf-8 -*-
# @Date    : 2018-11-24 15:39:14
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org

from django.contrib.syndication.views import Feed
from django.urls import reverse
from learning_logs.models import Topic


class LastestEntriesFeed(Feed):
    title = 'django ulysses topics'
    link = '/topics/'
    description = 'about new topics'

    def items(self):
        return Topic.objects.order_by('-date_added')[:5]

    def item_title(self, item):
        return item.text

    def item_owner(self, item):
        return item.owner

    # item_link is only needed if item has no get_absolute_url method
    # def item_link(self, item):
    #     return reverse('learning_logs:my_topics')

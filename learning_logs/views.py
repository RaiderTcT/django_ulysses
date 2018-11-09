from django.shortcuts import render
from django.http import HttpResponse, Http404,HttpResponseNotFound,HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Post
from .forms import TopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.core.cache import caches
import os
from django.template.loader import render_to_string
from django_ulysses.settings import BASE_DIR
from django.utils.translation import gettext as _
def index(request):
    # cache = caches['memcached']
    # key = cache.get_or_set('key_word', 'kyyyyy')
    # output = _('Weicome to my site')
    # Translators: This message appears on the home page only
    output = _('Weicome to my site')
    context = {'name':output}
    # static_html = f'{BASE_DIR}/learning_logs/templates/static_index.html'
    # if not os.path.exists(static_html):
    #     content = render_to_string('index.html', context)
    #     with open(static_html, 'w') as static_file:
    #         static_file.write(content)
    # return render(request, static_html)
    return render(request, 'index.html', context)

# 缓存时间15min
@cache_page(60 * 15, cache='filecached')
def topic(request, topic_id):
    """根据id访问topic的信息"""
    # id = request.GET.get('id', 4)
    try:
        t = Topic.objects.get(id=topic_id)
        posts = t.post_set.order_by('-date_added')
        context = {'topic': t, 'posts':posts, 'user':request.user}
        return render(request, 'topic.html', context)
    except Topic.DoesNotExist:
        return HttpResponseNotFound(f'<h1>Topic:{topic_id} not exist</h1>')

@cache_page(60 * 15, cache='filecached')
def topics(request):
    """全部的topics"""
    # 使用Paginator需要有排序
    topics = Topic.objects.order_by('-date_added')
    paginator = Paginator(topics, 10) # 每页25条
    try:
        page = request.GET.get('page')
    except InvalidPage:
        error_404 = _('Not find')
        raise Http404(error_404)
    topics = paginator.get_page(page) # 获取指定页面
    context = {'topics':topics}
    return render(request, 'topics.html', context)

@cache_page(60 * 15, cache='filecached')
@login_required
def my_topics(request):
    # 取当登录前用户创建的topic
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    paginator = Paginator(topics, 10) # 每页25条
    try:
        page = request.GET.get('page')
    except InvalidPage:
        error_404 = _('Not find')
        raise Http404(error_404)
    topics = paginator.get_page(page) # 获取指定页面
    context = {'topics':topics}
    return render(request, 'topics.html', context)


@login_required
def new_topic(request):
    """添加新的主题"""
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TopicForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # 添加数据到数据库
            topic = Topic(text=request.POST.get('text'), owner=request.user)

            topic.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('learning_logs:my_topics'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TopicForm()

    return render(request, 'new_topic.html', {'form': form})

@login_required
def new_post(request, topic_id):
    """添加新的主题"""
    # 在指定topic下创建post

    try:
        topic = Topic.objects.get(id=topic_id)
    except Topic.DoesNotExist:
        error_404 = _('Not this Blog')
        raise Http404(error_404)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PostForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # topic字段无法从表单获取，额外添加
            #　return an object that hasn’t yet been saved to the database
            new_post = form.save(commit=False)
            new_post.topic = topic
            # 在服务器上 进行转换， 只提交markdown文本原文
            # new_post.html_content = markdown(request.POST.get('text'),extensions=['markdown.extensions.extra',])
            new_post.owner = request.user
            new_post.save()
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = PostForm()
    context = {'form': form, 'topic': topic}
    return render(request, 'new_post.html', context=context)

@login_required
def edit_post(request, post_id):
    """修改现有的post"""
    # 获取要修改的post和其所属的topic
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        error_404 = _('No this post')
        raise Http404(error_404)
    topic = post.topic
    if post.owner != request.user:
        error_rights = _('You have no right to edit this post')
        raise Http404(error_rights)

    if request.method != "POST":
        # 初次请求，获取包含post数据的表单
        form = PostForm(instance=post)
    else:
        # Create a form to edit an existing Article, but use
        # POST data to populate the form.
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # post.html_content = markdown(form.cleaned_data['text'])
            post.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic.id,)))

    context = {'form': form, 'topic': topic, 'post': post}
    return render(request, 'edit_post.html', context)



def search(request):
    key_word = request.POST.get('key_word')
    if not key_word:
        warming_message = _('Please enter the query content')
        messages.add_message(request, messages.WARNING, warming_message)
        return HttpResponseRedirect(reverse('learning_logs:topics'))
    topics = Topic.objects.filter(text__contains=key_word).order_by('-date_added')
    # cache = caches['dbcached']
    # cache.set('key_word', key_word, 60*15)
    paginator = Paginator(topics, 10)  # 每页25条
    try:
        page = request.GET.get('page')
    except InvalidPage:
        error_404 = _('Not find')
        raise Http404(error_404)
    topics = paginator.get_page(page) # 获取指定页面
    context = {'topics':topics}
    return render(request, 'topics.html', context)

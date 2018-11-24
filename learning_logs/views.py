from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from .models import Topic, Post
from .forms import TopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from datetime import datetime
from django.contrib import messages
from django.views.decorators.cache import cache_page, never_cache
from django.core.cache import caches
import os
from django.template.loader import render_to_string
from django_ulysses.settings import BASE_DIR
from django.utils.translation import gettext as _
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator


class IndexView(View):
    """基于类的视图"""

    def get(self, request):
        return HttpResponse('get result')

    def post(self, request):
        return HttpResponse('post result')


def index(request):
    # Translators: This message appears on the home page only
    output = _('Weicome to my site')
    context = {'name': output}
    # static_html = f'{BASE_DIR}/learning_logs/templates/static_index.html'
    # if not os.path.exists(static_html):
    #     content = render_to_string('index.html', context)
    #     with open(static_html, 'w') as static_file:
    #         static_file.write(content)
    # return render(request, static_html)
    # index_logger.info('just for test')
    print(os.getenv('DJANGO_LOG_LEVEL'))
    return render(request, 'index.html', context)


class Topics(ListView):
    """基于类的视图，继承ListView显示topics列表"""
    # 指定模板
    template_name = 'topic_list.html'

    # model = Topic
    queryset = Topic.objects.order_by('-date_added')
    # 每页显示数量
    paginate_by = 10
    # 最后一页最多显示
    paginate_orphans = 15
    # 分页排序的标准
    # ordering = 'date_added'
    # 修改默认的object_list名称
    context_object_name = 'topic_list'

# @cache_page(60 * 15, cache='filecached')


def topics(request):
    """全部的topics"""
    # 使用Paginator需要有排序
    topics = Topic.objects.order_by('-date_added')
    paginator = Paginator(topics, 10)  # 每页25条
    try:
        page = request.GET.get('page')
    except InvalidPage:
        error_404 = _('Not find')
        raise Http404(error_404)
    topics = paginator.get_page(page)  # 获取指定页面
    context = {'topics': topics}
    return render(request, 'topics.html', context)


class MyTopics(Topics):
    """基于类的视图，继承Topics显示自己的topics"""

    def get_queryset(self):
        """筛选 作者为当前用户 返回queryset"""
        return Topic.objects.filter(owner=self.request.user).order_by('-date_added')


# @cache_page(60 * 15, cache='filecached')
@login_required
def my_topics(request):
    # 取当登录前用户创建的topic
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    paginator = Paginator(topics, 10)  # 每页25条
    try:
        page = request.GET.get('page')
    except InvalidPage:
        error_404 = _('Not find')
        raise Http404(error_404)
    topics = paginator.get_page(page)  # 获取指定页面
    context = {'topics': topics}
    return render(request, 'topics.html', context)


# 缓存时间15min
# @cache_page(60 * 15, cache='filecached')
def topic(request, topic_id):
    """根据id访问topic的信息"""
    # id = request.GET.get('id', 4)
    try:
        t = Topic.objects.get(id=topic_id)
        posts = t.post_set.order_by('-date_added')
        context = {'topic': t, 'posts': posts, 'user': request.user}
        return render(request, 'topic.html', context)
    except Topic.DoesNotExist:
        return HttpResponseNotFound(f'<h1>Topic:{topic_id} not exist</h1>')


# new_topic 的 基于类的视图
# 装饰一个类
decorators = [never_cache, login_required]
# @method_decorator(login_required, name='dispatch')
# @method_decorator(never_cache, name='dispatch')


@method_decorator(decorators, name='dispatch')
class TopicCreate(CreateView):
    """
    基于类的通用视图 
    """
    model = Topic
    fields = ['text']
    template_name = 'new_topic.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


@method_decorator(decorators, name='dispatch')
class NewtopicView(View):
    """
    基于类的视图
    """
    form_class = TopicForm
    initial = {}
    template_name = 'new_topic.html'

    # 装饰类的每一个实例
    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            topic = Topic(text=request.POST.get('text'), owner=request.user)
            topic.save()
            return redirect('learning_logs:my_topics')
        return render(request, self.template_name, {'form': form})


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
            return redirect('learning_logs:my_topics')
            # return HttpResponseRedirect(reverse('learning_logs:my_topics'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TopicForm()

    return render(request, 'new_topic.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class PostCreate(CreateView):
    model = Post
    template_name = 'new_post.html'
    fields = ['text']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


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
            return redirect('learning_logs:topic', topic_id=topic_id)
            # return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))

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
            return redirect('learning_logs:topic', topic_id=topic.id)
            # return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic.id,)))

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
    topics = paginator.get_page(page)  # 获取指定页面
    context = {'topics': topics}
    return render(request, 'topics.html', context)

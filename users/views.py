from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegisterForm
from django_ulysses.settings import EMAIL_HOST_USER
from users.tasks import send_register_email
from django.contrib import messages
# Create your views here.


def register(request):
    """注册用户"""
    if request.method != 'POST':
        # 显示空的注册表单
        # form = UserCreationForm()
        form = RegisterForm()
    else:
        # 提交填好的注册表
        # form = UserCreationForm(data=request.POST)
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # 注册后的用户 直接登录， 重定向到首页

            print(f"user: {EMAIL_HOST_USER}\n")
            authenticated_user = authenticate(username=new_user.username,
                                              password=request.POST.get('password1', ""))
            send_register_email.delay(new_user)
            messages.add_message(request, messages.INFO, '邮件已发送，请查收')
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request, 'register.html', context)


def my_login_view(request):
    """登录"""
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('learning_logs:index'))
            else:
                raise Http404('没有此用户')
    else:
        form = AuthenticationForm()
    context = {'form':form}
    return render(request, 'login.html', context)




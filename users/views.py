from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import RegisterForm
from django_ulysses.settings import EMAIL_HOST_USER
from users.tasks import send_register_email
from django.contrib import messages
from django_ulysses.settings import DANGER, PRIMARY
from .confirm import token_confirm
# Create your views here.

def confirm(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username).all()
        for user in users:
            user.delete()
        messages.add_message(request, DANGER, '验证码错误或已过期，请重新注册')
        return HttpResponseRedirect(reverse('learning_logs:index'))

    try:
        user =User.objects.get(username=username)
    except User.DoesNotExist:
        messages.add_message(request, DANGER, '没有此用户，请重新注册')
        return HttpResponseRedirect(reverse('learning_logs:index'))

    user.is_active = True
    user.save()
    login(request, user)
    messages.add_message(request, messages.SUCCESS, "验证成功，已登录")

    return HttpResponseRedirect(reverse('learning_logs:index'))

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
            new_user = form.save(commit=False)
            # 默认创建时is_active 是True
            new_user.is_active = False
            new_user.save()

            token = token_confirm.generate_validate_token(new_user.username)
            print(f"token:{token}")
            send_register_email.delay(new_user, token)
            messages.add_message(request, messages.INFO, '验证邮件已发送，请查收')

            # 注册后的用户 直接登录， 重定向到首页
            # authenticated_user = authenticate(username=new_user.username,
            #                                   password=request.POST.get('password1', ""))
            # login(request, authenticated_user)

            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request, 'register.html', context)



# def my_login_view(request):
#     """登录"""
#     if request.method == 'POST':
#         form = AuthenticationForm(request.POST)
#         if form.is_valid():
#             username = request.POST.get('username', '')
#             password = request.POST.get('password', '')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('learning_logs:index'))
#             else:
#                 raise Http404('没有此用户')
#     else:
#         form = AuthenticationForm()
#     context = {'form':form}
#     return render(request, 'login.html', context)




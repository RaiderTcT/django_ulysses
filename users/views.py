from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_ulysses.settings import DANGER, PRIMARY, EMAIL_HOST_USER
from .confirm import token_confirm
from .forms import RegisterForm, UserProfileForm
from users.tasks import send_register_email
from .models import UserProfile
from .my_email import my_send_mail
from django.utils.translation import gettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.utils.decorators import method_decorator
# Create your views here.


def confirm(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username).all()
        for user in users:
            user.delete()
        re_register_message = _('The verification code is incorrect or has expired. Please re-register')
        messages.add_message(request, DANGER, re_register_message)
        return HttpResponseRedirect(reverse('learning_logs:index'))

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        no_user_message = _('no this user please register')
        messages.add_message(request, DANGER, no_user_message)
        return HttpResponseRedirect(reverse('learning_logs:index'))

    user.is_active = True
    user.save()
    login(request, user)
    success_message = _('Successful verification')
    messages.add_message(request, messages.SUCCESS, success_message)

    return redirect('learning_logs:index')
    # return HttpResponseRedirect(reverse('learning_logs:index'))


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

            send_register_email.delay(new_user, token)
            # my_send_mail('注册', '验证',EMAIL_HOST_USER, [new_user.email])
            check_mail_message = _('Verification email has been sent, please check')
            messages.add_message(request, messages.INFO, check_mail_message)

            # 注册后的用户 直接登录， 重定向到首页
            # authenticated_user = authenticate(username=new_user.username,
            #                                   password=request.POST.get('password1', ""))
            # login(request, authenticated_user)
            return redirect('learning_logs:index')
            # return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request, 'register.html', context)


@method_decorator(login_required, name='dispatch')
class ProfileUpdate(UpdateView):
    model = UserProfile
    template_name = "edit_profile.html"
    # form_class = UserProfileForm
    fields = ['location', 'tel', 'about_me', 'avatar']


@login_required
def profile(request, user_id):
    """显示个人信息"""
    # 要查看的用户
    target_user = User.objects.get(id=user_id)
    # 当前用户
    user = request.user
    context = {'target_user': target_user, 'user': user}
    return render(request, 'user.html', context)


@login_required
def edit_profile(request, profile_id):
    """修改个人信息"""

    profile = get_object_or_404(UserProfile, id=profile_id)
    user = profile.user
    if user != request.user:
        raise Http404('请登录要修改的账户')

    if request.method != 'POST':
        # 使用数据库中查询得到profile创建表单
        form = UserProfileForm(instance=profile)
    else:
        # 测试浏览器是否支持cookie
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        #     messages.add_message(request, messages.INFO, '支持cookie')
        # else:
        #     messages.add_message(request, messages.INFO, '不支持cookie')

        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # cleaned_data 将输入数据规范化成合适的格式
            # profile.about_me = form.cleaned_data['about_me']
            # profile.location = form.cleaned_data['location']
            # profile.tel = form.cleaned_data['tel']
            form.save()
        return redirect('users:profile', user_id=user.id)
        # return HttpResponseRedirect(reverse('users:profile',args=(user_id,)))
    context = {'form': form, 'user': user}
    # request.session.set_test_cookie()
    return render(request, 'edit_profile.html', context)


@login_required
def upload_img(request):
    pass
    # avatar = Image.open(request.data[])


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


def create_profile():
    users = User.objects.filter(is_active=True)
    for user in users:
        new_profile = UserProfile(user=user)
        new_profile.save()

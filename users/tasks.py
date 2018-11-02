from django.core.mail import send_mail,send_mass_mail, EmailMultiAlternatives
from django.template import loader, Template
from celery import task
from django.conf import settings
from django.contrib.sites.models import Site
from django.urls import reverse
import absoluteuri
import os


@task
def send_register_email(user, token):

    subject, from_email, to = "[Django]验证用户", os.environ.get('EMAIL_HOST_USER', "2276777056@qq.com"), \
                              user.email

    # my_relative_url = f'/users/confirm/{token}'
    # url = absoluteuri.build_absolute_uri(my_relative_url)
    # url = absoluteuri.reverse('confirm', kwargs={'token':token})
    # 获取当前网站
    site = Site.objects.get_current()
    # 协议名：//域名/path
    url = '{protocol}://{domain}{path}'.format(
        protocol=getattr(settings, 'ABSOLUTEURI_PROTOCOL', 'http'),
        domain=site.domain,
        path= reverse('users:confirm', args=[token])
    )

    text_content = f"{user.username}，你好\
                    欢迎来到 Ulysses\
                    为了验证您的账户，请点击以下链接进行验证\
                    链接:{url}\
                    Ulysses\
                    请勿回复此邮件"

    html_template = loader.get_template('email/confirm.html')
    context = {'user':user, 'url':url}
    html_context = html_template.render(context)
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to])
    email.attach_alternative(html_context, 'text/html')
    # email.attach_alternative()
    # 添加附件
    # email.attach_file('users/templates/email/confirm.html', 'text/plain')
    # email.attach_file('users/templates/email/confirm.txt', 'text/html')
    email.send()
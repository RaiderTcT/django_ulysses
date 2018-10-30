from django.core.mail import send_mail,send_mass_mail, EmailMultiAlternatives
from django.template import loader, Template
from celery import task
from django_ulysses.settings import BASE_URL
import os


@task
def send_register_email(user, token):

    subject, from_email, to = "[Django]验证用户", os.environ.get('EMAIL_HOST_USER', "2276777056@qq.com"), \
                              user.email

    url = BASE_URL+f'users/confirm/{token}'

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
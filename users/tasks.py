from django.core.mail import send_mail,send_mass_mail, EmailMultiAlternatives
from celery import task
import os


@task
def send_register_email(user):

    subject, from_email, to = "注册", os.environ.get('EMAIL_HOST_USER', "2276777056@qq.com"), \
                              user.email
    text_content = "{{ user.username }}，你好\
                    欢迎来到 Ulysses\
                    为了验证您的账户，请点击以下链接进行验证\
                    链接\
                    Ulysses\
                    请勿回复此邮件"
    html_content = f"<p>{user.username}， 你好</p>\
                    <p>欢迎来到 <b>Ulysses</b>!</p>\
                    <p>为了验证您的账户，请点击进行验证</p>\
                    <p>或者您可以在浏览器被输入以下内容：</p>\
                    <p>链接</p>\
                    <p>Ulysses</p>\
                    <p><small>请勿回复此邮件</small></p>"
    email = EmailMultiAlternatives(subject=subject, body=text_content, from_email=from_email, to=[to])
    email.attach_alternative(html_content, 'text/html')
    # email.attach_alternative()
    # 添加附件
    email.attach_file('users/templates/email/confirm.html', 'text/plain')
    email.attach_file('users/templates/email/confirm.txt', 'text/html')
    email.send()
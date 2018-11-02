from django.core.mail import send_mail as core_send_mail
from django.core.mail import EmailMultiAlternatives
import threading

class MyEmailThread(threading.Thread):
    """多线程，发送邮件"""
    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html_message):
        threading.Thread.__init__(self)
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html_message = html_message

    # 发送邮件
    def run(self):
        mail = EmailMultiAlternatives(self.subject, self.body, self.from_email, self.recipient_list)
        if self.html_message :
            mail.attach_alternative(self.html_message, 'text/html')
        return mail.send(self.fail_silently)

# 创建线程 start 启动线程活动，会调用run方法
def my_send_mail(subject, body, from_email, recipient_list, fail_silently=False, html_message=None, *args, **kwargs):
    MyEmailThread(subject, body, from_email, recipient_list, fail_silently, html_message).start()
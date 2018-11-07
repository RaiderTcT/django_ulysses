from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


# class User(AbstractUser):
#     """
#     Users within the Django authentication system are represented by this
#     model.
#
#     Username and password are required. Other fields are optional.
#     """
#     location = models.CharField('地址', max_length=64, blank=True)
#     tel = models.CharField('联系方式', max_length=50, blank=True)
#     about_me = models.TextField('关于我')
#     mod_date = models.DateTimeField('上次修改日期', auto_now=True)
#
#
#     def __str__(self):
#         return f"username：{self.username}"



class UserProfile(models.Model):
    """为已经使用了内置User模型的项目来拓展用户模型 """
    # user对象可使用 user.userprofile, 或 user.proflie 得到用户信息
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField('地址', max_length=64, blank=True)
    tel = models.CharField('联系方式', max_length=50, blank=True)
    about_me = models.TextField('关于我')
    mod_date = models.DateTimeField('上次修改日期', auto_now=True)
    avatar = models.ImageField('用户头像', upload_to='avatar/%Y/%m/%d', default='avatar/wenhuang.jpg',blank=True, null=True)

    class Meta:
        verbose_name = "用户信息"
        app_label = 'users'


    def __str__(self):
        return f"{self.user.__str__()}'s profile"

# 在接收到user对象被保存后的信号时 创建一个profile
# sender: 发出信号的模型
# instance: 正保存的实例
#　created：True if a new record was created.
@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False,**kwargs):
    if created:
        # Return a tuple of (object, created)
        profile, created = UserProfile.objects.get_or_create(user=instance)



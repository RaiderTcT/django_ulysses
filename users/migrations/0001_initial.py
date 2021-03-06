# Generated by Django 2.1.2 on 2018-11-08 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=64, verbose_name='地址')),
                ('tel', models.CharField(blank=True, max_length=50, verbose_name='联系方式')),
                ('about_me', models.TextField(verbose_name='关于我')),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name='上次修改日期')),
                ('avatar', models.ImageField(blank=True, default='avatar/wenhuang.jpg', null=True, upload_to='avatar/%Y/%m/%d', verbose_name='用户头像')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '用户信息',
            },
        ),
    ]

# Generated by Django 2.1.2 on 2018-11-18 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_auto_20181108_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=255)),
                ('topic', models.ManyToManyField(to='learning_logs.Topic')),
            ],
        ),
    ]
# Generated by Django 2.1.2 on 2018-11-01 13:21

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0008_post_html_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=mdeditor.fields.MDTextField(),
        ),
    ]
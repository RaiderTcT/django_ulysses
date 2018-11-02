"""
WSGI config for django_ulysses project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""


# Django使用DJANGO_SETTINGS_MODULE环境变量来定位合适的settings模块
# 如果此变量未设置，默认的wsgi.py设置其为mysite.settings，mysite是你的项目
# 因为环境变量是进程级的，如果你在相同进程运行多个Django站点，这将不能正常工作。这在mod_wsgi中可能发生。

import os
from os.path import join, dirname, abspath

PROJECT_DIR = dirname(dirname(abspath(__file__)))  # 3
import sys  # 4

sys.path.insert(0, PROJECT_DIR)  # 5

os.environ["DJANGO_SETTINGS_MODULE"] = "django_ulysses.settings"  # 7

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
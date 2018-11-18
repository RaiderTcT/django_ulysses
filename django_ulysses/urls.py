"""django_ulysses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap, index
from .sitemaps import TopicSitemap, PostSitemap
from learning_logs.models import Topic, Post
from django.contrib.sitemaps import GenericSitemap
sitemaps = {
    'Topic': TopicSitemap,
}
info_dict = {
    'queryset': Topic.objects.all(),
    'date_field': 'date_added'
}

urlpatterns = i18n_patterns(
    path(r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls', namespace='learning_logs')),
    path('users/', include('users.urls', namespace='users')),
    path('sitemap.xml', index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 在url加前缀 en-us zh-hans
# urlpatterns += i18n_patterns(
#     path('', include('learning_logs.urls', namespace='learning_logs')),
# )
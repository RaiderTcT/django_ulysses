from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import register
app_name = 'users'
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'),  name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register/', register, name='register'),
]

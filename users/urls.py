from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from .views import register, confirm, edit_profile, profile, ProfileUpdate, ProfileCreate

app_name = 'users'
urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='index.html'), name='logout'),
    path('register/', register, name='register'),
    re_path(r"^confirm/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$", confirm, name='confirm'),
    # path('edit_profile/<profile_id>', edit_profile, name='edit_profile'),
    path('edit_profile/<int:pk>', ProfileUpdate.as_view(), name='edit_profile'),
    path('profile/<user_id>', profile, name='profile'),

]

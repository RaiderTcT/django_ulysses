from django.forms import EmailField, Textarea
from django.forms.models import ModelForm
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from users.models import UserProfile


class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}


class UserProfileForm(ModelForm):

    class Meta:
        model = UserProfile
        fields = ('location', 'tel', 'about_me')
        widgets = {
            'about_me': Textarea(attrs={'cols': 80}),
        }


# class LoginForm(Form):
#     username = CharField(label='Username:', max_length=20)
#     password = CharField(label='Password:', max_length=20)
#     widgets = {'password':PasswordInput}

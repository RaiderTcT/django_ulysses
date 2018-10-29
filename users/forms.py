from django.forms import Form, CharField, PasswordInput, EmailField
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = EmailField()

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}




# class LoginForm(Form):
#     username = CharField(label='Username:', max_length=20)
#     password = CharField(label='Password:', max_length=20)
#     widgets = {'password':PasswordInput}

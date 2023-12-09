from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Usuario, CustomUser
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')  

class CustomUserChangeForm (UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email= forms.EmailField(required=True)
    

    class Meta:
        model = User
        fields = ('username', 'first_name','last_name','email', 'password1', 'password2')

class AdminUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('staff', 'Supervisor'),
        ('normal', 'Normal'),
    )

    role = forms.ChoiceField(choices=ROLE_CHOICES)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2", 'role')
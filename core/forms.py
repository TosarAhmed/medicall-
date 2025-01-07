from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from core.models import UserOTP 

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    password = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

class SignupForm (UserCreationForm):
    mobile = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your Mobile Number',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(widget = forms.TextInput(attrs={
        'placeholder': 'Your Username',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    email = forms.CharField(widget = forms.EmailInput(attrs={
        'placeholder': 'Your Email Address',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    password1 = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    password2 = forms.CharField(widget = forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'w-full px-4 py-3 rounded-xl'
    }))

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Save the mobile field in a separate model (e.g., UserOTP)
            UserOTP.objects.create(user=user, mobile=self.cleaned_data['mobile'])
        return user
from django import forms

from account.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50,
                               label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Username'}),
                               required=False)
    phone_number = forms.CharField(max_length=13, label="",
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control',
                                              'placeholder': 'Telefon raqamingizni kiriting'}),
                                   required=False)
    email = forms.EmailInput()

    password1 = forms.CharField(
        label="",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control',
                                          'placeholder': 'Parol kiriting'}),
        help_text=False,
        required=False,
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control',
                                          'placeholder': 'Parolni tasdiqlang'}),
        strip=False,
        help_text=False,
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password1', 'password2']
        labels = {'email': ""}
        widgets = {'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': "Emailinginizni kiriting"})}


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          "autofocus": True,
                                          'placeholder': 'Username'}),
                               required=False)
    password = forms.CharField(max_length=50, label="", strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', "autocomplete": "current-password",
                                          'placeholder': 'Parol'}),
                               required=False)


class UserDetailsForm(forms.ModelForm):
    class Meta:
        User.username.help_text = ''
        model = User
        labels = {'username': "", 'first_name': "", 'last_name': "", 'phone_number': "", 'email': ''}
        fields = ['username', 'phone_number', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ismingiz'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Familiyangiz'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Elektron pochtangiz'})
        }

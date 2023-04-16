from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput, min_length=8, max_length=20)

class SignUpForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.CharField(label="password", widget=forms.PasswordInput(), min_length=8, max_length=20)
    
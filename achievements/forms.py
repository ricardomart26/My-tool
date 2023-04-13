from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.PasswordInput()

class SignUpForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    email = forms.EmailField(label="email", required=True)
    password = forms.PasswordInput()
    
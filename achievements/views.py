from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
# from pprint import pprint as pp

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from django.contrib.auth.hashers import make_password

from achievements.decorators import user_not_authenticated, user_authenticated
from achievements.models import Achievement, Student
from achievements.forms import LoginForm, SignUpForm
from achievements.achievement_api import get_achievements

def index(request: HttpRequest, id):
    print(id)
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {"achievement_list": achievement_list})

# @user_authenticated
def home(request: HttpRequest):
    achievement_list = Achievement.objects.all()
    if not achievement_list.exists():
        get_achievements()
    return render(request, 'achievements/home.html', {
        "achievement_list": achievement_list,
        "user": request.user
        })

@user_authenticated
def logout_user(request: HttpRequest):
    logout(request)
    return redirect('home')

@user_not_authenticated
def login_user(request: HttpRequest):
    if request.method == 'POST':
        f = LoginForm(request.POST)
        if f.is_valid():
            username: str = f.cleaned_data["username"]
            encoded_password: str = make_password(f.cleaned_data["password"])
            user = authenticate(username=username, password=encoded_password)
            if user is not None:
                print("Authentication successful")
                return redirect('home')
            else:
                print("Authentication failed")
                return redirect('login_user')
        else:
            print("Authentication failed, form not valid")
            return render(request, 'achievements/login.html', {"form": LoginForm, "error": "Form is invalid"})
    if request.method == 'GET':
        return render(request, 'achievements/login.html', {"form": LoginForm})
    return HttpResponseNotAllowed(f"<h1> Method {request.method.lower()} not allowed")


@user_not_authenticated(None, 'home')
def signup_user(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            encoded_password: str = make_password(form.cleaned_data["password"])
            email: str = form.cleaned_data["email"]
            try:
                user: User = User.objects.create(username=username, email=email, password=encoded_password)
            except Exception as e:
                return render(request, 'achievements/signup.html', {'form': SignUpForm, "error": e})
            user.save()
            return render(request, 'achievements/login.html', {"form": LoginForm})
    if request.method == 'GET':
        return render(request, 'achievements/signup.html', {"form": SignUpForm})
    return HttpResponseNotAllowed(f"<h1> Method {request.method.lower()} not allowed")


def get_user_by_username(request: HttpRequest, username: str):
    user = Student.objects.get(username=username)
    user_achievements: list[Achievement] = user.achievements.all()
    if request.method == 'GET':
        return render(request, 'achievements/user_info.html', {'user': user, "achievements": user_achievements})
    return HttpResponseNotAllowed(f"<h1> Method {request.method.lower()} not allowed")
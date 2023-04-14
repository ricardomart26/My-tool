from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, HttpResponseNotAllowed
from achievements.models import Achievement
from pprint import pprint as pp
from achievements.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from achievements.decorators import user_not_authenticated, user_authenticated
from django.shortcuts import redirect


def index(request: HttpRequest, id):
    print(id)
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {"achievement_list": achievement_list})


@user_authenticated
def home(request: HttpRequest):
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {
        "achievement_list": achievement_list,
        "achievement_list_size": len(achievement_list),
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
            password: str = f.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                return redirect('home')    
            else:
                return redirect('login_user')
                # return render(request, 'achievements/login.html', {"form": LoginForm, "error": "User or password wrong"})
        else:
            return render(request, 'achievements/login.html', {"form": LoginForm, "error": "Form is invalid"})
    if request.method == 'GET':
        return render(request, 'achievements/login.html', {"form": LoginForm})
    return HttpResponseNotAllowed(f"<h1> Method {request.method.lower()} not allowed")


@user_not_authenticated(None, 'home')
def signup_user(request: HttpRequest):
    print("Entrou!")
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password"]
            email: str = form.cleaned_data["email"]
            try:
                user: User = User.objects.create(username=username, email=email, password=password)
            except Exception as e:
                if e == "UNIQUE constraint failed: auth_user.username":
                    return render(request, 'achievements/signup.html', {'form': SignUpForm, "error": "Username already in use"})
                return render(request, 'achievements/signup.html', {'form': SignUpForm, "error": e})
            user.save()
            return render(request, 'achievements/login.html', {"form": LoginForm})
    if request.method == 'GET':
        return render(request, 'achievements/signup.html', {"form": SignUpForm})
    return HttpResponseNotAllowed(f"<h1> Method {request.method.lower()} not allowed")
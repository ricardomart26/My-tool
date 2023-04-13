from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from achievements.models import Achievement
from pprint import pprint as pp
from achievements.forms import LoginForm, SignUpForm
from django.contrib.auth.models import User


def index(request: HttpRequest, id):
    print(id)
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {"achievement_list": achievement_list})

def home(request: HttpRequest):
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {
        "achievement_list": achievement_list,
        "achievement_list_size": len(achievement_list)
        })

def login(request: HttpRequest):

    return render(request, 'achievements/login.html', {"form": LoginForm})

def signup(request: HttpRequest):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password"]
            email: str = form.cleaned_data["email"]
            user: User = User.objects.create(username, email, password)
            user.save()
            return HttpResponse({'success': True})
    return render(request, 'achievements/signup.html', {"form": SignUpForm})
from django.shortcuts import render
from django.http import HttpResponse
from achievements.models import Achievement
from pprint import pprint as pp




def index(request, id):
    print(id)
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {"achievement_list": achievement_list})

def home(request):
    achievement_list = Achievement.objects.all()
    return render(request, 'achievements/home.html', {
        "achievement_list": achievement_list,
        "achievement_list_size": len(achievement_list)
        })

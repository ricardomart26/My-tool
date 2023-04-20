from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("", views.home, name="home"),
    path("login", views.login_user, name="login_user"),
    path("signup", views.signup_user, name="signup_user"),
    path("logout", views.logout_user, name="logout_user"),
    path("user/<string:username>", views.get_user_by_username, name="username_view")
]
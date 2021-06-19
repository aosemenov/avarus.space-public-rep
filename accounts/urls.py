from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('password_reset/', views.passwordPage, name="password_reset"),
    path('', views.home, name="home"),
]

from django.urls import path

from main import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view()),
    path('login/', views.LoginView.as_view())
]

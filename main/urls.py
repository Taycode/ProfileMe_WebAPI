from django.urls import path

from main import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('profile/', views.ProfileView.as_view()),
    path('profile/links/', views.ProfileLinksView.as_view()),

]

from django.urls import path
from .views import LoginView, LogoutView, UserCreateView


urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
]

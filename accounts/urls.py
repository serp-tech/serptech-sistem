from django.urls import path
from .views import LoginView, LogoutView, UserCreateView, ProfileDetailView, ProfileUpdateView


urlpatterns = [
    path('login/', LoginView, name='login'),
    path('logout/', LogoutView, name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('perfil/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('perfil/<int:pk>/update', ProfileUpdateView.as_view(), name='profile_update'),
]

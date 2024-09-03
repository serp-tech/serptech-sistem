from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile


def LoginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            login_form = AuthenticationForm()
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': login_form})


def LogoutView(request):
    logout(request)
    return redirect('login')



class UserCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/requester/'


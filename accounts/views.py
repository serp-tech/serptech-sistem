from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from .forms import CustomUserCreationForm, CustomUserChangeForm


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



class UserCreateView(PermissionRequiredMixin, CreateView):
    
    model = User
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = '/requester/'
    permission_required = 'accounts.add_userprofile'


class ProfileDetailView(LoginRequiredMixin, DetailView):

    model = User
    template_name = 'perfil_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = UserProfile.objects.get(user=self.request.user)
        return context
    
    def get_object(self):
        return self.request.user
    

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    form_class = CustomUserChangeForm
    template_name = 'perfil_update.html'
    

    def get_object(self):
        return self.request.user
    
    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.request.user.pk})

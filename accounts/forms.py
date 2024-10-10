from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import UserProfile, OFFICE_STATUS
from stock.models import Sector, Unit

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    profile_image = forms.ImageField(required=False)
    sector = forms.ModelMultipleChoiceField(queryset=Sector.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    unit = forms.ModelMultipleChoiceField(queryset=Unit.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    position = forms.ChoiceField(choices=OFFICE_STATUS, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name",
                  "password1", "password2", "profile_image", "sector", "unit", "position")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        if commit:
            user.save()
            # Verificar se o UserProfile já existe
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                user_profile = UserProfile(user=user)
            
            # Atualizar ou criar o UserProfile
            user_profile.profile_image = self.cleaned_data.get('profile_image')
            user_profile.position = self.cleaned_data.get('position')
            user_profile.save()

            # Atribuir os setores e unidades
            user_profile.sector.set(self.cleaned_data.get('sector'))
            user_profile.unit.set(self.cleaned_data.get('unit'))

        return user


class CustomUserChangeForm(UserChangeForm):
    
    profile_image = forms.ImageField(required=False)
    current_password = forms.CharField(
        label='Senha Atual',
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        required=False,
    )
    new_password = forms.CharField(
        label='Nova Senha',
        widget=forms.PasswordInput,
        required=False,
    )
    confirm_password = forms.CharField(
        label='Confirmar Nova Senha',
        widget=forms.PasswordInput,
        required=False,
    )
    
    class Meta:
        model = User
        fields = ("profile_image", "username", "email", "first_name", "last_name",)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if current_password:
            if not check_password(current_password, self.instance.password):
                raise ValidationError("A senha atual está incorreta.")
        return current_password
    
    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError('As novas senhas não coincidem.')
            
        return cleaned_data


    def save(self, commit=True):
        user = super(CustomUserChangeForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
                    
        if commit:
            user.save()
            
            # Atualizar ou criar o perfil do usuário
            user_profile, created = UserProfile.objects.get_or_create(user=user)

            # Atualiza a imagem de perfil apenas se uma nova imagem foi fornecida
            if self.cleaned_data.get('profile_image'):
                user_profile.profile_image = self.cleaned_data.get('profile_image')
            
            user_profile.save()

        return user

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields.pop('password', None)


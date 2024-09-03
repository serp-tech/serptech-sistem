from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
            user_profile = UserProfile(
                user=user,
                profile_image=self.cleaned_data.get('profile_image'),
                position=self.cleaned_data.get('position'),
            )
            user_profile.save()

            # Agora atribuimos os setores utilizando o método set()
            user_profile.sector.set(self.cleaned_data.get('sector'))
            user_profile.unit.set(self.cleaned_data.get('unit'))

        return user

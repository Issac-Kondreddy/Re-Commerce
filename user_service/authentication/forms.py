from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'first_name', 'last_name', 'dob', 'address', 'gender', 'phone_number']


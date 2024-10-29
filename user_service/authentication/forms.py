from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        help_text="Upload a JPEG or PNG image only."
    )

    phone_number = PhoneNumberField(
        widget=forms.TextInput(attrs={'placeholder': '+12125552368'}),
        help_text="Enter in international format, e.g., +12125552368"
    )

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get("profile_picture", False)
        if profile_picture:
            if profile_picture.content_type not in ["image/jpeg", "image/png"]:
                raise ValidationError("Only JPEG or PNG files are allowed.")
        return profile_picture

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'dob', 'address', 'phone_number', 'gender', 'profile_picture']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD', 'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'style': 'display: none;'}),
        }
        labels = {
            'profile_picture': '',
        }


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




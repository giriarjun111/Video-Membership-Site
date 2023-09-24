from django import forms
from .models import UserProfile

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']  # Add any other fields you want the user to be able to update

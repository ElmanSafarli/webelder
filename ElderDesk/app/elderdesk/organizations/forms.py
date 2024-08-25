from django import forms
from .models import Organization, UserProfile

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'domains']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'domains': forms.TextInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'email', 'user_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'user_type': forms.Select(attrs={'class': 'form-control'}),
        }
# forms.py
from django import forms
from .models import UserProfile


class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'user_type']

# forms.py
from django import forms


class FeedbackForm(forms.Form):
    feedback = forms.CharField(widget=forms.Textarea)

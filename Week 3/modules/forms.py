# modules/forms.py

from django import forms

class ModuleQueryForm(forms.Form):
    query = forms.CharField(
        label='Ask About Modules',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your query here...'
        })
    )

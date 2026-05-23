from django import forms
from .models import Scholarship

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model  = Scholarship
        fields = ['name', 'provider', 'deadline', 'country', 'level', 'requirements', 'benefits']
        widgets = {
            'deadline':     forms.DateInput(attrs={'type': 'date'}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'benefits':     forms.Textarea(attrs={'rows': 4}),
        }
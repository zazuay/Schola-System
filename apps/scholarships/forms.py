from django import forms
from .models import Scholarship
from django.utils import timezone

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model  = Scholarship
        fields = ['name', 'provider', 'deadline', 'country', 'level', 'requirements', 'benefits']
        widgets = {
            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),
            'requirements': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'List scholarship requirements...'
                }
            ),

            'benefits': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Describe scholarship benefits...'
                }
            )
                    }
        
def clean_deadline(self):
    deadline = self.cleaned_data['deadline']

    if deadline < timezone.now().date():
        raise forms.ValidationError(
            'Deadline cannot be in the past.'
        )

    return deadline
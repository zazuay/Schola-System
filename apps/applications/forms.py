from django import forms
from .models import Application, Document
import os

ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/png']
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = []   # user & scholarship set in view
        widgets = {
            'type': forms.Select(
                attrs={'class': 'form-select'}
            ),
            'file': forms.FileInput(
                attrs={'class': 'form-control'}
            ),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ['type', 'file']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            if f.content_type not in ALLOWED_TYPES:
                raise forms.ValidationError('Allowed format: PDF, JPG, JPEG, PNG.')
            if f.size > MAX_SIZE_BYTES:
                raise forms.ValidationError('File must be under 5 MB.')
            ext = os.path.splitext(f.name)[1].lower()
            allowed_extensions = ['.pdf', '.jpg', '.jpeg', '.png']

            if ext not in allowed_extensions:
                raise forms.ValidationError('Invalid file extensions.')
        return f
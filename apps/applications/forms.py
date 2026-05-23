from django import forms
from .models import Application, Document

ALLOWED_TYPES = ['application/pdf', 'image/jpeg', 'image/png']
MAX_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB


class ApplicationForm(forms.ModelForm):
    class Meta:
        model  = Application
        fields = []   # user & scholarship set in view


class DocumentForm(forms.ModelForm):
    class Meta:
        model  = Document
        fields = ['type', 'file']

    def clean_file(self):
        f = self.cleaned_data.get('file')
        if f:
            if f.content_type not in ALLOWED_TYPES:
                raise forms.ValidationError('Only PDF, JPG, or PNG files are allowed.')
            if f.size > MAX_SIZE_BYTES:
                raise forms.ValidationError('File must be under 5 MB.')
        return f
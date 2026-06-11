from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    password  = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model  = CustomUser
        fields = ['name', 'email', 'phone']  # ← remove 'password' from here

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if not re.fullmatch(r'^\d{10,15}$', phone):
            raise forms.ValidationError(
                "Phone number must contain 10-15 digits."
            )

        return phone
    
    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError("Passwords do not match.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'student'
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
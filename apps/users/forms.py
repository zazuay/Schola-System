from django import forms
from django.contrib.auth.forms import AuthenticationForm
import re
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'new-password'
        }),
        label='Confirm Password'
    )

    class Meta:
        model  = CustomUser
        fields = ['name', 'email', 'phone']  # ← remove 'password' from here

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        if phone and not re.fullmatch(r'^\d{10,15}$', phone):
            raise forms.ValidationError(
                "Phone number must contain 10-15 digits."
            )

        return phone
    
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError(
                "Password must be at least 8 characters."
            )
        validate_password(password)
        
        return password
    
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
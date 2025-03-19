from django import forms
from django.contrib.auth.models import User
from .models import User as CustomUser, Credential

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'lastname', 'credit']


class CredentialForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) 
    confirm_password = forms.CharField(widget=forms.PasswordInput)  

    class Meta:
        model = Credential
        fields = ['email', 'password']  

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Le password non corrispondono")

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
from .models import Blog, PokerRoom
from django import forms
# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "content"]


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists() and email != self.instance.email:
            raise forms.ValidationError("Email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class PokerForm(forms.ModelForm):
    class Meta:
        model = PokerRoom
        fields = ["name", "is_private", "password"]
        widgets = {
            "password" : forms.PasswordInput()
        }

    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get("is_private")
        password = cleaned_data.get("password")

        if is_private and not password:
            self.add_error("password", "Private rooms must have a password")
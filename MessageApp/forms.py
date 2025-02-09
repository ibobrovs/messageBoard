from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Listing


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "content", "category"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите заголовок"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Введите текст объявления"}),
            "category": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Заголовок",
            "content": "Текст объявления",
            "category": "Категория",
        }
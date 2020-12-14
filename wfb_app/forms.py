from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Units, Profile, GameResults


class AddUnit(forms.ModelForm):
    class Meta:
        model = Units
        fields = "__all__"
        labels = {
            "name": "Nazwa",
            "offensive": "Offensive Skill",
            "strength": "Siła",
            "ap": "Armour Piercing",
            "reflex": "Czy ma Lightning Reflexes",
            "armys": "Armia"
        }


class LogForm(forms.Form):
    login = forms.CharField(max_length=64, label="Login")
    password = forms.CharField(max_length=64, label="Haslo", widget=forms.PasswordInput)


class RegisterUserForm(forms.ModelForm):
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz hasło")
    class Meta:
        model = User
        fields = ["username", "password", "password_2", "email"]
        widgets = {"password": forms.PasswordInput}
        labels = {
            "username": "Nickname",
            "password": "Hasło",
            "email": "Podaj email"
        }
    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data["username"]
    #     if User.objects.filter(username=username).exists():
    #         raise ValidationError("Login zajety")
    #     password = cleaned_data["password"]
    #     password_2 = cleaned_data["password_2"]
    #     if password != password_2:
    #         raise ValidationError("Hasla sie nie zgadzaja")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user_army"]
        labels = {"user_army": "Wybierz Armie"}


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Nickname",
            "email": "Podaj email"
        }


class GameResultsForm(forms.ModelForm):
    class Meta:
        model = GameResults
        fields = ["battle_points", "objective", "objective_type", "game_rank", "opponent"]
        labels = {
            "user": "Nick",
            "battle_points": "Punkty",
            "objective": "Czy Objective wykonany",
            "objective_type": "Jaki Objective",
            "game_rank": "Ranga turnieju",
            "opponent": "Przeciwnik",
            "date": "Data"
        }
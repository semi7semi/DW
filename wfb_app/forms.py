from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from .models import Units, Profile, GameResults


class AddUnit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddUnit, self).__init__(*args, **kwargs)
        self.fields["ap"].widget.attrs["min"] = 0
        self.fields["ap"].widget.attrs["max"] = 10
        self.fields["strength"].widget.attrs["min"] = 1
        self.fields["strength"].widget.attrs["max"] = 10
        self.fields["offensive"].widget.attrs["min"] = 1
        self.fields["offensive"].widget.attrs["max"] = 10

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
    password = forms.CharField(widget=forms.PasswordInput, label="Nowe hasło")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Powtórz nowe hasło")
    class Meta:
        model = User
        fields = ["username", "email"]
        labels = {
            "username": "Nickname",
            "email": "Podaj email",
        }


class GameResultsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GameResultsForm, self).__init__(*args, **kwargs)
        self.fields["battle_points"].widget.attrs["min"] = 0
        self.fields["battle_points"].widget.attrs["max"] = 20


    class Meta:
        model = GameResults
        fields = ["battle_points", "army", "objective", "objective_type", "game_rank","opponent_dw", "opponent", "opponent_army", "date"]
        labels = {
            "user": "Nick",
            "army": "Czym Grałeś",
            "battle_points": "Punkty",
            "objective": "Czy Objective wykonany",
            "objective_type": "Jaki Objective",
            "game_rank": "Ranga turnieju",
            "opponent_dw": "Przeciwnik z DW",
            "opponent": "Inny przeciwnik",
            "opponent_army": "Armia przeciwnika",
            "date": "Data"
        }
        help_texts = {
            "date": " RRRR-MM-DD",
        }


class CalcForm(forms.Form):
    unit_name1 = forms.ModelChoiceField(queryset=Units.objects.all(), label="Nazwa Jednostki")
    unit_name2 = forms.ModelChoiceField(queryset=Units.objects.all(), label="Nazwa Jednostki", required=False)
    attacks = forms.IntegerField(min_value=1, max_value=100, label = "Podaj ilosc atakow")
    defensive = forms.IntegerField(min_value=1, max_value=10, label="Podaj Defensive Skill")
    resistance = forms.IntegerField(min_value=1, max_value=10, label="Podaj Resistance")

class DiceRollForm(forms.Form):
    no_of_dice = forms.IntegerField(min_value=1, max_value=100, label="Ile kości?")
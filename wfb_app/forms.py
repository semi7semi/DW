from django import forms
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe

from .models import Units, Profile, GameResults, Parings_3, Parings_5, Armys


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
    code = forms.CharField(label="Hasło Wałeczków", help_text=" Udowodnij, że jestes Wałeczkiem")
    class Meta:
        model = User
        fields = ["username", "password", "password_2", "email", "code"]
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
    obj_opo = forms.BooleanField(label="Przeciwnik", required=False)
    some_text = forms.BooleanField(label="Kto wykonal Objective", disabled=True, required=False)
    class Meta:
        model = GameResults
        fields = ["battle_points", "army", "some_text", "objective", "obj_opo", "objective_type", "game_rank","opponent_dw", "opponent", "opponent_army", "date"]
        labels = {
            "user": "Nick",
            "army": "Czym Grałeś",
            "battle_points": "Punkty",
            "objective": "Ja",
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
    attacks1 = forms.IntegerField(min_value=1, max_value=100, label="Podaj ilosc atakow")
    unit_name2 = forms.ModelChoiceField(queryset=Units.objects.all(), label="Nazwa Jednostki")
    attacks2 = forms.IntegerField(min_value=1, max_value=100, label = "Podaj ilosc atakow")
    defensive = forms.IntegerField(min_value=1, max_value=10, label="Podaj Defensive Skill")
    resistance = forms.IntegerField(min_value=1, max_value=10, label="Podaj Resistance")

class DiceRollForm(forms.Form):
    no_of_dice = forms.IntegerField(min_value=1, max_value=100, label="Ile kości?")


class FirstParingsForm(forms.Form):
    first_p1 = forms.ModelChoiceField(queryset=Armys.objects.all(), label="Wystawka")
    first_op1 = forms.ModelChoiceField(queryset=Armys.objects.all(), label="Dostawka przeciwnikow")
    first_p2 = forms.ModelChoiceField(queryset=Armys.objects.all(), label="Dostawka")
    first_op2 = forms.ModelChoiceField(queryset=Armys.objects.all(), label="Wystawka przeciwnikow")


class ParingsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ParingsForm, self).__init__(*args, **kwargs)
        for i in ["p11", "p12", "p13", "p21", "p22", "p23", "p31", "p32", "p33"]:
            self.fields[i].widget.attrs["min"] = -2
            self.fields[i].widget.attrs["max"] = 2
    class Meta():
        model = Parings_3
        fields = ["name", "p1", "p2", "p3", "op1", "op2", "op3", "p11", "p12", "p13", "p21", "p22", "p23", "p31", "p32", "p33"]
        labels = {
            "name": "Nazwa",
            "p1": "Gracz 1",
            "p2": "Gracz 2",
            "p3": "Gracz 3",
            "op1": "Przeciwnik 1",
            "op2": "Przeciwnik 2",
            "op3": "przeciwnik 3",
        }


class Parings5Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Parings5Form, self).__init__(*args, **kwargs)
        for i in ["p11", "p12", "p13", "p14", "p15", "p21", "p22", "p23", "p24", "p25", "p31", "p32", "p33", "p34", "p35", "p41", "p42", "p43", "p44", "p45", "p51", "p52", "p53", "p54", "p55"]:
            self.fields[i].widget.attrs["min"] = -2
            self.fields[i].widget.attrs["max"] = 2
    class Meta():
        model = Parings_5
        fields = ["name", "p1", "p2", "p3", "p4", "p5", "op1", "op2", "op3", "op4", "op5", "p11", "p12", "p13", "p14", "p15", "p21", "p22", "p23", "p24", "p25", "p31", "p32", "p33", "p34", "p35", "p41", "p42", "p43", "p44", "p45", "p51", "p52", "p53", "p54", "p55"]
        labels = {
            "name": "Nazwa",
            "p1": "Gracz 1",
            "p2": "Gracz 2",
            "p3": "Gracz 3",
            "p4": "Gracz 4",
            "p5": "Gracz 5",
            "op1": "Przeciwnik 1",
            "op2": "Przeciwnik 2",
            "op3": "przeciwnik 3",
            "op4": "Przeciwnik 4",
            "op5": "przeciwnik 5",
        }
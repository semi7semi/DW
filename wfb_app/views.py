from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView, ListView

from functions import towound, afterarmour
from wfb_app.forms import AddUnit, LogForm, RegisterUserForm, ProfileForm, EditUserForm, GameResultsForm
from wfb_app.models import Units, Armys, GameResults, Objectives, Profile
from django.contrib.auth.models import User


class Index(View):
    # strona główna, 5ciu najleprzysz graczy, logowanie, linki
    def get(self, request):
        result = []
        users = User.objects.all()
        no_of_games = GameResults.objects.all().count()
        for user in users:
            games = GameResults.objects.filter(user=user)
            total = 0
            for game in games:
                total += game.battle_points
            #  user.id bo przy sortowaniu tych samych wynikow python nie ogarnia :)
            result.append([total, user.id, user])
        result.sort(reverse=True)
        result = result[:5]
        ctx = {"no_of_users": users.count(), "no_of_games": no_of_games, "result": result}
        return render(request, "index.html", ctx)


class Calc(LoginRequiredMixin, View):
    # Funkcjionalnosc Kalkulator, wylicza statystyke walki przy podanych parametrach przez uzytkownika
    # tylko dla zalogowanych
    def get(self, request):
        units_list = Units.objects.all()
        return render(request, "calculator.html", {"units_list": units_list})
    def post(self, request):
        unit_id = request.POST.get('name')
        attacks = int(request.POST.get('attacks'))
        defensive = int(request.POST.get('defensive'))
        resistance = int(request.POST.get('resistance'))
        if request.POST.get('option') == "fight":
            unit = Units.objects.get(pk=unit_id)
            if unit.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if unit.offensive - defensive >= 4:
                x = 5 / 6
            elif 4 > unit.offensive - defensive >= 0:
                x = 2 / 3
            elif unit.offensive - defensive <= -4:
                x = 1 / 3
            else:
                x = 1 / 2
            hit = attacks * (x + ref)
            if x + ref == 1:
                hit = attacks * x
            wounds = towound(hit, unit.strength, resistance)
            saves = ["none", "6+", "5+", "4+", "3+", "2+", "1+"]
            arm = []
            for armour in range(0, 7):
                wounds_after_armour = afterarmour(unit.ap, armour, wounds)
                arm.append(wounds_after_armour)
            ctx = {
                    "hit": round(hit, 2),
                    "wounds": round(wounds, 2),
                    "arm": arm,
                    "saves": saves,
                    "unit": unit
                }
            return render(request, "calculator.html", ctx)


class List(LoginRequiredMixin, View):
    # Lista wszystkich oddzialow, nie zaleznie od armii
    # tylko dla zalogowanych
    def get(self, request):
        units_list = Units.objects.all().order_by("name")
        return render(request, "units_list.html", {"units_list": units_list})


class AddUnitView(LoginRequiredMixin, View):
    # dodanawnie nowej jednostki do DB
    # tylko dla zalogowanych
    def get(self, request):
        form = AddUnit()
        ctx = {"form": form}
        return render(request, "add_unit.html", ctx)
    def post(self, request):
        form = AddUnit(request.POST)
        if form.is_valid():
            form.save()
            return redirect("calc-view")


class EditUnitView(LoginRequiredMixin, View):
    # Edycja jednostki i zapis do DB
    # tylko dla zalogowanych
    def get(self, request, id):
        unit = Units.objects.get(pk=id)
        form = AddUnit(instance=unit)
        ctx = {"form": form}
        return render(request, "edit_unit.html", ctx)
    def post(self, request, id):
        unit = get_object_or_404(Units, pk=id)
        form = AddUnit(request.POST, instance=unit)
        if form.is_valid():
            form.save()
            return redirect("units-list")


class DeleteUnitView(LoginRequiredMixin, View):
    # Usuwanie jednostki z DB
    # tylko dla zalogowanych
    def get(self, request, id):
        unit = Units.objects.get(pk=id)
        unit.delete()
        return redirect("calc-view")


class ArmyListView(LoginRequiredMixin, View):
    # lista wszystkich dostepnych armii
    # linki do poszczegolnych jednostek armijnych
    # tylko dla zalogowanych
    def get(self, request):
        army_list = Armys.objects.all().order_by("name")
        return render(request, "army_list.html", {"army_list": army_list})


class ArmyDetailsView(LoginRequiredMixin, View):
    # szczegoly armii, wszystkie jednostki dodane dla danej armii
    # tylko dla zalogowanych
    def get(selfself, request, id):
        army = Armys.objects.get(pk=id)
        units = Units.objects.filter(army=army.id)
        ctx = {"army": army, "units": units}
        return render(request, "army_details.html", ctx)


class LoginView(FormView):
    # logowanie i authentykacja
    form_class = LogForm
    template_name = "login_form.html"
    success_url = "/"

    def form_valid(self, form):
        username = form.cleaned_data["login"]
        password = form.cleaned_data["password"]
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        form.add_error(None, "Zły login lub haslo")
        return super().form_invalid(form)


class LogoutView(View):
    # wylogowanie
    def get(self, request):
        logout(request)
        return redirect("/")


class CreateUserView(View):
    # Rejestracja nowego uzytkownika
    def get(self, request):
        form = RegisterUserForm()
        profile_form = ProfileForm()
        ctx = {"form": form, "profile_form": profile_form}
        return render(request, "user_form.html", ctx)
    def post(self, request):
        form = RegisterUserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data["password"])
            user.save()
            user_army = profile_form.cleaned_data["user_army"]
            Profile.objects.create(
                user_army = user_army,
                user = user
            )
            return redirect("users-list")
        else:
            ctx = {"form": form, "profile_form": profile_form}
            return render(request, "user_form.html", ctx)


class EditUserView(LoginRequiredMixin, View):
    # edycja konta urzytkownika, email, armia
    def get(selfself, request, id):
        user = User.objects.get(pk=id)
        form = EditUserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)
        return render(request, "user_form.html", {
            "form": form,
            "profile_form": profile_form
        })
    def post(self, request, id):
        user = User.objects.get(pk=id)
        form = EditUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            return redirect("users-list")


class UsersList(LoginRequiredMixin, ListView):
    # lista zarejestrowanych uzytkownikow
    # tylko dla zalogowanych
    model = User
    context_object_name = "users"
    ordering = "username"


class UserDetailsView(View):
    # Szczegoly uzytkownika, wszsytkie bitwy, punkty, armia
    def get(self, request, id):
        user = User.objects.get(pk=id)
        ranking = GameResults.objects.filter(user=user).order_by("-date")
        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details.html", ctx)


class DeleteUser(LoginRequiredMixin, View):
    # usuwanie uzytkownika
    # tylko dla mnie

    # musze zabezpieczyc jeszcze!!!!
    def get(self, request, id):
        user = User.objects.get(pk=id)
        user.delete()
        return redirect("users-list")


class RankingList(View):
    # Ranking wszsytkich uzytkownikow, z punktami
    # sortowanie po wynikach, rangze itd
    def get(self, request):
        ranking = GameResults.objects.all()
        return render(request, "ranking_list.html", {"ranking": ranking})
    def post(self, request):
        if request.POST.get("option") == "name_sort":
            ranking = GameResults.objects.all().order_by("user", "-battle_points")
            return render(request, "ranking_list.html", {"ranking": ranking})
        if request.POST.get("option") == "points_sort":
            ranking = GameResults.objects.all().order_by("-battle_points")
            return render(request, "ranking_list.html", {"ranking": ranking})
        if request.POST.get("option") == "rank_sort":
            ranking = GameResults.objects.all().order_by("-game_rank", "-date")
            return render(request, "ranking_list.html", {"ranking": ranking})
        else:
            ranking = GameResults.objects.all()
            return render(request, "ranking_list.html", {"ranking": ranking})


class AddGameResultView(LoginRequiredMixin, View):
    # dodawanie nowych wynikow do rankingu
    # tylko dla zalogowanych
    def get(self, request):
        form = GameResultsForm()
        ctx = {"form": form}
        return render(request, "ranking_form.html", ctx)
    def post(self, request):
        form = GameResultsForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            return redirect("ranking-list")
        else:
            ctx = {"form": form}
            return render(request, "ranking_form.html", ctx)

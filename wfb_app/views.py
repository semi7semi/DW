

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from datetime import datetime
from functions import towound, afterarmour, sort_count, sort_rv
from wfb_app.forms import AddUnit, LogForm, RegisterUserForm, ProfileForm, EditUserForm, GameResultsForm, CalcForm
from wfb_app.models import Units, Armys, GameResults, Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator

class Landing_page(View):
    def get(self, request):
        no_of_games = GameResults.objects.all().count()
        no_of_users = User.objects.all().exclude(username="admin").count()
        users = User.objects.all().exclude(username="admin")
        count_master = GameResults.objects.filter(game_rank="master").count()
        count_local = GameResults.objects.filter(game_rank="local").count()
        count_home = GameResults.objects.filter(game_rank="home").count()
        ctx = {
            "no_of_games": no_of_games,
            "no_of_users": no_of_users,
            "count_master": count_master,
            "count_local": count_local,
            "count_home": count_home,
            "users": users
        }
        return render(request, "dashboard.html", ctx)


class Index(View):
    # strona główna, 5ciu najleprzysz graczy, logowanie, linki
    def get(self, request):
        result = []
        users = User.objects.all().exclude(username="admin")
        no_of_games = GameResults.objects.all().count()
        for user in users:
            games = GameResults.objects.filter(user=user)
            count_master = games.filter(game_rank="master").count()
            count_local = games.filter(game_rank="local").count()
            count_home = games.filter(game_rank="home").count()
            total = 0
            total_master = 0
            total_local = 0
            total_home = 0
            ranking_points = 0
            count = count_master + count_local + count_home
            for game in games:
                if game.game_rank == "master":
                    total_master += game.battle_points
                elif game.game_rank == "local":
                    total_local += game.battle_points
                elif game.game_rank == "home":
                    total_home += game.battle_points
                total = total_master + total_local + total_home
            if count_master == 0:
                m = 0
            else:
                m = total_master / count_master
            if count_local == 0:
                l = 0
            else:
                l = total_local / count_local
            if count_home == 0:
                h = 0
            else:
                h = total_home / count_home
            ranking_points += (m * 3) + l + (h * 0.33)
            #  user.id bo przy sortowaniu tych samych wynikow python nie ogarnia :)
            result.append([
                round(m, 2),
                round(l, 2),
                round(h,2),
                round(ranking_points, 2),
                total,
                count,
                user.id,
                user,
                count_master,
                count_local,
                count_home
            ])
        result.sort(reverse=True)
        result_by_count = sorted(result)
        result_by_count.sort(key=sort_count, reverse=True)
        result_by_rv = sorted(result)
        result_by_rv.sort(key=sort_rv, reverse=True)
        ctx = {
            "no_of_users": users.count(),
            "no_of_games": no_of_games,
            "result": result,
            "best_gen_id": result_by_rv[0][6],
            "best_gamer_id": result_by_count[0][6],
            "best_veg_id": result_by_rv[-1][6]
        }
        return render(request, "index.html", ctx)


class CalcView(LoginRequiredMixin, View):
    def get(self, request):
        form = CalcForm(initial={"attacks":10, "defensive":4, "resistance":3})
        ctx = {"form": form}
        return render(request, "calc.html", ctx)
    def post(self, request):
        form = CalcForm(request.POST)
        if form.is_valid():
            unit = form.cleaned_data["unit_name"]
            attacks = form.cleaned_data["attacks"]
            defensive = form.cleaned_data["defensive"]
            resistance = form.cleaned_data["resistance"]
            if unit.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if unit.offensive - defensive >= 4:
                x = 5 / 6
            elif 4 > unit.offensive - defensive > 0:
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
                "attacks": attacks,
                "hit": round(hit, 2),
                "wounds": round(wounds, 3),
                "armour": arm,
                "saves": saves,
                "unit": unit
            }
            return render(request, "calc.html", ctx)


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
            army = form.cleaned_data["army"]
            form.save()
            return redirect("army-details", id=army.id)


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
            army = form.cleaned_data["army"]
            form.save()
            return redirect("army-details", id=army.id)


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
        army_data = []
        list = []
        for army in army_list:
            units_no = Units.objects.filter(army=army).count()
            army_data = [army, units_no]
            list.append(army_data)
        return render(request, "army_list.html", {"list": list})


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
        return render(request, "edit_user.html", {
            "form": form,
            "profile_form": profile_form
        })
    def post(self, request, id):
        user = User.objects.get(pk=id)
        form = EditUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid() and profile_form.is_valid():
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]
            if password == password2:
                user = form.save()
                user.set_password(password)
                user.save()
                profile_form.save()
                return redirect("users-list")
            else:
                return render(request, "edit_user.html", {
                    "form": form,
                    "profile_form": profile_form,
                    "error": "Hasla musza byc takie same"
                })



class UsersList(LoginRequiredMixin, View):
    # Lista wszystkich uzytkownkow
    # tylko dla zalogowanych
    def get(self, request):
        users = User.objects.all().order_by("username").exclude(username="admin")
        return render(request, "user_list.html", {"users": users})


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
    def post(self, request, id):
        user = User.objects.get(pk=id)
        sort_option = request.POST.get("sort_option")
        desc = request.POST.get("desc")
        if desc == "+":
            desc = ""
        ranking = GameResults.objects.all().filter(user=user).order_by(f"{desc}{sort_option}")
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


def Pages(request, ranking):
    # Stronicowanie
    paginator = Paginator(ranking, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return page_obj


class RankingList(View):
    # Ranking wszsytkich uzytkownikow, z punktami
    # sortowanie po wynikach, randze itd
    def get(self, request):
        ranking = GameResults.objects.all().order_by("-date", "-id")
        return render(request, "ranking_list.html", {"ranking": Pages(request, ranking)})
    def post(self, request):
        sort_option = request.POST.get("sort_option")
        sort_option_sec = request.POST.get("sort_option_sec")
        desc = request.POST.get("desc")
        desc2 = request.POST.get("desc2")
        if desc == "+":
            desc = ""
        if desc2 == "+":
            desc2 = ""
        if sort_option == sort_option_sec:
            ranking = GameResults.objects.all().order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.all().order_by(f"{desc}{sort_option}", f"{desc2}{sort_option_sec}")
        return render(request, "ranking_list.html", {"ranking": Pages(request, ranking)})


class AddGameResultView(LoginRequiredMixin, View):
    # dodawanie nowych wynikow do rankingu
    # tylko dla zalogowanych
    def get(self, request):
        form = GameResultsForm(initial={"date": datetime.now()})
        ctx = {"form": form}
        return render(request, "ranking_form.html", ctx)
    def post(self, request):
        form = GameResultsForm(request.POST)
        if form.is_valid():
            # opponent = form.cleaned_data["opponent"]
            # opp = User.objects.filter(username=opponent)
            result = form.save(commit=False)
            result.user = request.user
            result.save()
            # if opp.exists():
            #     print(f"{opp} istnieje")
            return redirect("ranking-list")
        else:
            ctx = {"form": form}
            return render(request, "ranking_form.html", ctx)


class EditGameResultView(View):
    def get(self, request, id):
        game = GameResults.objects.get(pk=id)
        form = GameResultsForm(instance=game)
        ctx = {"form": form}
        return render(request, "edit_ranking.html", ctx)
    def post(self, request, id):
        game = get_object_or_404(GameResults, pk=id)
        form = GameResultsForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect("user-details", id=game.user.id)

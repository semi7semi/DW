

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from datetime import datetime
from functions import towound, afterarmour, sort_count, sort_rv
from wfb_app.forms import AddUnit, LogForm, RegisterUserForm, ProfileForm, EditUserForm, GameResultsForm, CalcForm, \
    DiceRollForm
from wfb_app.models import Units, Armys, GameResults, Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum
import random

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
        max = [5, 10, 20]
        for user in users:
            games = GameResults.objects.filter(user=user)
            master = games.filter(game_rank="master")
            local = games.filter(game_rank="local")
            home = games.filter(game_rank="home")
            count_master = master.count()
            count_local = local.count()
            count_home = home.count()
            total_masters = master.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            total_locals = local.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            total_homes = home.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            best_masters = master.order_by("-battle_points")[:max[0]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            best_locals = local.order_by("-battle_points")[:max[1]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            best_homes = home.order_by("-battle_points")[:max[2]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            total = total_masters + total_locals + total_homes
            count = count_master + count_local + count_home
            ranking_points = best_masters + best_locals + best_homes
            result.append([
                ranking_points,
                total,
                count,
                total_masters,
                best_masters,
                count_master,
                total_locals,
                best_locals,
                count_local,
                total_homes,
                best_homes,
                count_home,
                user.id,
                user,
            ])
        result.sort(reverse=True)
        result_by_count = sorted(result)
        result_by_count.sort(key=sort_count, reverse=True)
        # result_by_rv = sorted(result)
        # result_by_rv.sort(key=sort_rv, reverse=True)
        ctx = {
            "no_of_users": users.count(),
            "no_of_games": no_of_games,
            "result": result,
            "best_gen_id": result[0][12],
            "best_gamer_id": result_by_count[0][12],
            "best_veg_id": result[-1][12],
            "max": max
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


class RollDiceView(View):
    def get(self, request):
        form = DiceRollForm(initial={"no_of_dice":10})
        ctx = {"form": form}
        return render(request, "dices.html", ctx)
    def post(self, request):
        form = DiceRollForm(request.POST)
        if form.is_valid():
            no_of_dices = form.cleaned_data["no_of_dice"]
            rolls = []
            sill = None
            for i in range(no_of_dices):
                dice = random.randint(1, 6)
                rolls.append(dice)
            rolls.sort()
            plus2 = rolls.count(2) + rolls.count(3) + rolls.count(4) + rolls.count(5) +rolls.count(6)
            plus3 = rolls.count(3) + rolls.count(4) + rolls.count(5) +rolls.count(6)
            plus4 = rolls.count(4) + rolls.count(5) + rolls.count(6)
            plus5 = rolls.count(5) + rolls.count(6)
            plus6 = rolls.count(6)
            if no_of_dices > 3 and no_of_dices == plus6:
                sill = "Sill style!"
            ctx = {
                "rolls": rolls,
                "plus2": plus2,
                "plus3": plus3,
                "plus4": plus4,
                "plus5": plus5,
                "plus6": plus6,
                "sill": sill

            }
            return render(request, "dices.html", ctx)


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
        sort_option_sec = request.POST.get("sort_option_sec")
        desc = request.POST.get("desc")
        desc2 = request.POST.get("desc2")
        search_option = request.POST.get("search_option")
        search_word = request.POST.get("search_word")
        if desc == "+":
            desc = ""
        if desc2 == "+":
            desc2 = ""
        # if search_option == "opponent":
        #     ranking = GameResults.objects.filter(user=user).filter(opponent__icontains=search_word)

        if sort_option == sort_option_sec:
            ranking = GameResults.objects.all().filter(user=user).order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.all().filter(user=user).order_by(f"{desc}{sort_option}", f"{desc2}{sort_option_sec}")
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

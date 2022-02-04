from itertools import permutations
from operator import itemgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import FormView
from datetime import datetime
from functions import towound, afterarmour, sort_count, sort_rv
from wfb_app.forms import AddUnit, LogForm, RegisterUserForm, ProfileForm, EditUserForm, GameResultsForm, CalcForm, \
    DiceRollForm, ParingsForm, Parings5Form, FirstParingsForm, Parings4Form, TournamentsForm, TParings3Form, \
    TParings4Form, TParings5Form, ArmyIconForm
from wfb_app.models import Units, Armys, GameResults, Profile, Parings_3, Parings_5, Parings_4, Tournaments, Team_of_3, \
    Team_of_4, Team_of_5
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum
import random

MAX_GAMES = [5, 10, 20]
GAMES_YEAR = GameResults.objects.all().filter(date__year=2022)


class Landing_page(View):
    def get(self, request):
        no_of_games = GAMES_YEAR.count()
        no_of_users = User.objects.all().exclude(username="admin").count()
        users = User.objects.all().exclude(username="admin").order_by("username")
        count_master = GAMES_YEAR.filter(game_rank="master").count()
        count_local = GAMES_YEAR.filter(game_rank="local").count()
        count_home = GAMES_YEAR.filter(game_rank="home").count()
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
        no_of_games = GAMES_YEAR.count()
        max = MAX_GAMES
        for user in users:
            games = GAMES_YEAR.filter(user=user)
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
            if count_master == 0:
                av_master = 0
            else:
                av_master = round(total_masters / count_master, 1)
            if count_local == 0:
                av_local = 0
            else:
                av_local = round(total_locals / count_local, 1)
            if count_home == 0:
                av_home = 0
            else:
                av_home = round(total_homes / count_home, 1)

            total = total_masters + total_locals + total_homes
            count = count_master + count_local + count_home
            ranking_points = best_masters + best_locals + best_homes
            result.append([
                ranking_points,
                total,
                count,
                best_masters,
                total_masters,
                count_master,
                av_master,

                best_locals,
                total_locals,
                count_local,
                av_local,

                best_homes,
                total_homes,
                count_home,
                av_home,
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
            "best_gen_id": result[0][15],
            "best_gamer_id": result_by_count[0][15],
            "best_veg_id": result[-1][15],
            "max": max
        }
        return render(request, "index.html", ctx)


class Index_2021(View):
    # strona główna, 5ciu najleprzysz graczy, logowanie, linki
    def get(self, request):
        result = []
        users = User.objects.all().exclude(username="admin")
        no_of_games = GameResults.objects.filter(date__year=2021).count()
        max = MAX_GAMES
        for user in users:
            games = GameResults.objects.filter(date__year=2021).filter(user=user)
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
            if count_master == 0:
                av_master = 0
            else:
                av_master = round(total_masters / count_master, 1)
            if count_local == 0:
                av_local = 0
            else:
                av_local = round(total_locals / count_local, 1)
            if count_home == 0:
                av_home = 0
            else:
                av_home = round(total_homes / count_home, 1)

            total = total_masters + total_locals + total_homes
            count = count_master + count_local + count_home
            ranking_points = best_masters + best_locals + best_homes
            result.append([
                ranking_points,
                total,
                count,
                best_masters,
                total_masters,
                count_master,
                av_master,

                best_locals,
                total_locals,
                count_local,
                av_local,

                best_homes,
                total_homes,
                count_home,
                av_home,
                user.id,
                user,
            ])
        result.sort(reverse=True)
        result_by_count = sorted(result)
        result_by_count.sort(key=sort_count, reverse=True)
        ctx = {
            "no_of_users": users.count(),
            "no_of_games": no_of_games,
            "result": result,
            "best_gen_id": result[0][15],
            "best_gamer_id": result_by_count[0][15],
            "best_veg_id": result[-1][15],
            "max": max
        }
        return render(request, "index_2021.html", ctx)


class Index_2020(View):
    # strona główna, logowanie, linki
    def get(self, request):
        result = []
        users = User.objects.all().exclude(username="admin")
        no_of_games = GameResults.objects.filter(date__year=2020).count()
        max = MAX_GAMES
        for user in users:
            games = GameResults.objects.filter(date__year=2020).filter(user=user)
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
            if count_master == 0:
                av_master = 0
            else:
                av_master = round(total_masters / count_master, 1)
            if count_local == 0:
                av_local = 0
            else:
                av_local = round(total_locals / count_local, 1)
            if count_home == 0:
                av_home = 0
            else:
                av_home = round(total_homes / count_home, 1)

            total = total_masters + total_locals + total_homes
            count = count_master + count_local + count_home
            ranking_points = best_masters + best_locals + best_homes
            result.append([
                ranking_points,
                total,
                count,
                best_masters,
                total_masters,
                count_master,
                av_master,

                best_locals,
                total_locals,
                count_local,
                av_local,

                best_homes,
                total_homes,
                count_home,
                av_home,
                user.id,
                user,
            ])
        result.sort(reverse=True)
        result_by_count = sorted(result)
        result_by_count.sort(key=sort_count, reverse=True)
        ctx = {
            "no_of_users": users.count(),
            "no_of_games": no_of_games,
            "result": result,
            "best_gen_id": result[0][15],
            "best_gamer_id": result_by_count[0][15],
            "best_veg_id": result[-1][15],
            "max": max
        }
        return render(request, "index_2020.html", ctx)


class CalcView(LoginRequiredMixin, View):
    def get(self, request):
        form = CalcForm(initial={"attacks":10, "defensive":4, "resistance":3})
        ctx = {"form": form}
        return render(request, "calc.html", ctx)
    def post(self, request):
        form = CalcForm(request.POST)
        if form.is_valid():
            unit1 = form.cleaned_data["unit_name1"]
            attacks1 = form.cleaned_data["attacks1"]
            unit2 = form.cleaned_data["unit_name2"]
            attacks2 = form.cleaned_data["attacks2"]
            defensive = form.cleaned_data["defensive"]
            resistance = form.cleaned_data["resistance"]
            saves = ["none", "6+", "5+", "4+", "3+", "2+", "1+"]
            if unit1.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if unit1.offensive - defensive >= 4:
                x = 5 / 6
            elif 4 > unit1.offensive - defensive > 0:
                x = 2 / 3
            elif unit1.offensive - defensive <= -4:
                x = 1 / 3
            else:
                x = 1 / 2
            hit = attacks1 * (x + ref)
            if x + ref == 1:
                hit = attacks1 * x
            wounds = towound(hit, unit1.strength, resistance)
            arm = []
            for armour in range(0, 7):
                wounds_after_armour = afterarmour(unit1.ap, armour, wounds)
                arm.append(wounds_after_armour)
            # Dla drugiej
            if unit2.reflex:
                ref = 1 / 6
            else:
                ref = 0
            if unit2.offensive - defensive >= 4:
                x = 5 / 6
            elif 4 > unit2.offensive - defensive > 0:
                x = 2 / 3
            elif unit2.offensive - defensive <= -4:
                x = 1 / 3
            else:
                x = 1 / 2
            hit2 = attacks2 * (x + ref)
            if x + ref == 1:
                hit2 = attacks2 * x
            wounds2 = towound(hit2, unit2.strength, resistance)
            arm2 = []
            for armour in range(0, 7):
                wounds_after_armour2 = afterarmour(unit2.ap, armour, wounds2)
                arm2.append(wounds_after_armour2)
            ctx = {
                "attacks1": attacks1,
                "hit": round(hit, 2),
                "wounds": round(wounds, 3),
                "armour": arm,
                "saves": saves,
                "unit1": unit1,
                "attacks2": attacks2,
                "hit2": round(hit2, 2),
                "wounds2": round(wounds2, 3),
                "armour2": arm2,
                "unit2": unit2,
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
            total = sum(rolls)
            if no_of_dices > 2 and no_of_dices == plus6:
                sill = "Sill style!"
            ctx = {
                "rolls": rolls,
                "plus2": plus2,
                "plus3": plus3,
                "plus4": plus4,
                "plus5": plus5,
                "plus6": plus6,
                "total": total,
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
            code = form.cleaned_data["code"]
            if code == "jajco":
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
                return redirect("register")
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
        ranking = GAMES_YEAR.filter(user=user).order_by("-date")
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
        if desc == "+":
            desc = ""
        if desc2 == "+":
            desc2 = ""

        if sort_option == sort_option_sec:
            ranking = GAMES_YEAR.filter(user=user).order_by(f"{desc}{sort_option}")
        else:
            ranking = GAMES_YEAR.filter(user=user).order_by(f"{desc}{sort_option}",
                                                                           f"{desc2}{sort_option_sec}")
        if request.method == "POST" and "best_masters" in request.POST:
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="master").order_by("-battle_points")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="local").order_by("-battle_points")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="home").order_by("-battle_points")[:MAX_GAMES[2]]

        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details.html", ctx)


class UserDetailsView_2021(View):
    # Szczegoly uzytkownika, wszsytkie bitwy, punkty, armia
    def get(self, request, id):
        user = User.objects.get(pk=id)
        ranking = GameResults.objects.filter(date__year=2021).filter(user=user).order_by("-date")
        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details_2021.html", ctx)
    def post(self, request, id):
        user = User.objects.get(pk=id)
        sort_option = request.POST.get("sort_option")
        sort_option_sec = request.POST.get("sort_option_sec")
        desc = request.POST.get("desc")
        desc2 = request.POST.get("desc2")
        if desc == "+":
            desc = ""
        if desc2 == "+":
            desc2 = ""

        if sort_option == sort_option_sec:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).order_by(f"{desc}{sort_option}",
                                                                           f"{desc2}{sort_option_sec}")
        if request.method == "POST" and "best_masters" in request.POST:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="master").order_by("-battle_points")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="local").order_by("-battle_points")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="home").order_by("-battle_points")[:MAX_GAMES[2]]

        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details_2021.html", ctx)


class UserDetailsView_2020(View):
    # Szczegoly uzytkownika, wszsytkie bitwy, punkty, armia
    def get(self, request, id):
        user = User.objects.get(pk=id)
        ranking = GameResults.objects.filter(date__year=2020).filter(user=user).order_by("-date")
        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details_2020.html", ctx)
    def post(self, request, id):
        user = User.objects.get(pk=id)
        sort_option = request.POST.get("sort_option")
        sort_option_sec = request.POST.get("sort_option_sec")
        desc = request.POST.get("desc")
        desc2 = request.POST.get("desc2")
        if desc == "+":
            desc = ""
        if desc2 == "+":
            desc2 = ""

        if sort_option == sort_option_sec:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).order_by(f"{desc}{sort_option}",
                                                                           f"{desc2}{sort_option_sec}")
        if request.method == "POST" and "best_masters" in request.POST:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="master").order_by("-battle_points")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="local").order_by("-battle_points")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="home").order_by("-battle_points")[:MAX_GAMES[2]]

        total = 0
        for score in ranking:
            total += score.battle_points
        ctx = {"ranking": ranking, "total": total, "user": user}
        return render(request, "user_details_2020.html", ctx)


class DeleteUser(LoginRequiredMixin, View):
    # usuwanie uzytkownika
    # tylko dla mnie
    def get(self, request, id):
        user = User.objects.get(pk=id)
        ctx = {
            "user": user
        }
        return render(request, "delete_user.html", ctx)
    # musze zabezpieczyc jeszcze!!!!
    def post(self, request, id):
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
        ranking = GAMES_YEAR.order_by("-date", "-id")
        return render(request, "ranking_list.html", {"ranking": Pages(request, ranking)})
    def post(self, request):
        if request.method == "POST" and "2020" in request.POST:
            return redirect("ranking-list-2020")
        if request.method == "POST" and "2021" in request.POST:
            return redirect("ranking-list-2021")
        # if request.method == "POST" and "2022" in request.POST:
        #     return redirect("ranking-list-2022")
        if request.method == "POST" and "sort" in request.POST:
            sort_option = request.POST.get("sort_option")
            sort_option_sec = request.POST.get("sort_option_sec")
            desc = request.POST.get("desc")
            desc2 = request.POST.get("desc2")
            if desc == "+":
                desc = ""
            if desc2 == "+":
                desc2 = ""
            if sort_option == sort_option_sec:
                ranking = GAMES_YEAR.order_by(f"{desc}{sort_option}")
            else:
                ranking = GAMES_YEAR.order_by(f"{desc}{sort_option}", f"{desc2}{sort_option_sec}")
            return render(request, "ranking_list.html", {"ranking": Pages(request, ranking)})


class RankingList_2021(View):
    # ranking archiwalny
    def get(self, request):
        ranking = GameResults.objects.filter(date__year=2021).order_by("-date", "-id")
        return render(request, "ranking_list_2021.html", {"ranking": Pages(request, ranking)})

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
            ranking = GameResults.objects.filter(date__year=2021).order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.filter(date__year=2021).order_by(f"{desc}{sort_option}", f"{desc2}{sort_option_sec}")

        if request.method == "POST" and "2021" in request.POST:
            return redirect("ranking-list")

        return render(request, "ranking_list_2021.html", {"ranking": Pages(request, ranking)})



class RankingList_2020(View):
    # ranking archiwalny
    def get(self, request):
        ranking = GameResults.objects.filter(date__year=2020).order_by("-date", "-id")
        return render(request, "ranking_list_2020.html", {"ranking": Pages(request, ranking)})

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
            ranking = GameResults.objects.filter(date__year=2020).order_by(f"{desc}{sort_option}")
        else:
            ranking = GameResults.objects.filter(date__year=2020).order_by(f"{desc}{sort_option}", f"{desc2}{sort_option_sec}")

        if request.method == "POST" and "2021" in request.POST:
            return redirect("ranking-list")

        return render(request, "ranking_list_2020.html", {"ranking": Pages(request, ranking)})

        # elif request.method == "POST" and "search" in request.POST:
        #     search_option = request.POST.get("search_option")
        #     search_text = request.POST.get("search_text")
        #     print(search_option)
        #     print(search_text)
        #     if search_option == "user":
        #         ranking = GameResults.objects.filter(user__icontains=search_text)
        #     elif search_option == "opponent_dw":
        #         ranking = GameResults.objects.filter(opponent_de__icontains=search_text)
        #     elif search_option == "game_rank":
        #         ranking = GameResults.objects.filter(game_rank__icontains=search_text)
        #     elif search_option == "battle_points":
        #         ranking = GameResults.objects.filter(battle_points__icontains=search_text)
        #     elif search_option == "army":
        #         ranking = GameResults.objects.filter(army__icontains=search_text)
        #     elif search_option == "opponent_army":
        #         ranking = GameResults.objects.filter(opponent_army__icontains=search_text)
        #     else:
        #         ranking = GameResults.objects.all()
        #     return render(request, "index.html")

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
            user = request.user
            army = form.cleaned_data["army"]
            battle_points = form.cleaned_data["battle_points"]
            objective = form.cleaned_data["objective"]
            obj_opo = form.cleaned_data["obj_opo"]
            objective_type = form.cleaned_data["objective_type"]
            game_rank = form.cleaned_data["game_rank"]
            opponent_dw = form.cleaned_data["opponent_dw"]
            opponent = form.cleaned_data["opponent"]
            opponent_army = form.cleaned_data["opponent_army"]
            date = form.cleaned_data["date"]
            if opponent == None:
                result = form.save(commit=False)
                result.user = request.user
                result.save()
            # Dla przeciwnika:
                GameResults.objects.create(
                        user = opponent_dw,
                        army = opponent_army,
                        battle_points = 20 - battle_points,
                        objective = obj_opo,
                        objective_type = objective_type,
                        game_rank = game_rank,
                        opponent_dw = user,
                        opponent = opponent,
                        opponent_army = army,
                        date = date
                    )
            elif opponent_dw == None:
                result = form.save(commit=False)
                result.user = request.user
                result.save()
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


class TableView(View):
    def get(self, request):
        # Charge chart
        range_data = range(2, 13)
        charge = [100, 97, 92, 83, 72, 58, 42, 28, 17, 8, 3]
        charge_s = [100, 99, 98, 95, 89, 81, 68, 52, 36, 20, 7]
        charge_rr = [100, 99, 99, 97, 92, 83, 66, 48, 31, 16, 5]
        charge_s_rr = [100, 99, 99, 99, 99, 96, 90, 77, 59, 36, 14]
        # Discipline chart
        range_disc = range(2, 11)
        dis = [3, 8, 17, 28, 42, 58, 72, 83, 92]
        dis_rr = [5, 16, 31, 48, 66, 83, 92, 97, 99]
        dis_min = [7, 20, 36, 52, 68, 81, 89, 95, 98]
        dis_max = [1, 2, 5, 11, 19, 32, 48, 64, 80]
        dis_min_rr = [14, 36, 59, 77, 90, 96, 99, 99, 99]
        dis_max_rr = [1, 4, 10, 20, 35, 54, 73, 87, 96]
        # Casting chart
        range_cast = range(3, 19)
        dice1 = [67, 50, 33, 17]
        dice2 = [97, 92, 83, 72, 58, 42, 28, 17, 8, 3]
        dice3 = [99, 99, 98, 95, 91, 84, 74, 63, 50, 38, 26, 16, 10, 5, 2, 1]
        dice4 = [98, 98, 98, 98, 98, 97, 94, 90, 84, 76, 66, 56, 44, 34, 24, 16]
        dice5 = [100, 100, 100, 99, 99, 99, 99, 98, 97, 94, 90, 85, 78, 70, 60, 50]
        miscast = [3, 10, 21]
        ctx = {
            "range_data": range_data,
            "charge": charge,
            "charge_s": charge_s,
            "charge_rr": charge_rr,
            "charge_s_rr": charge_s_rr,

            "range_disc": range_disc,
            "dis": dis,
            "dis_rr": dis_rr,
            "dis_min": dis_min,
            "dis_max": dis_max,
            "dis_min_rr": dis_min_rr,
            "dis_max_rr": dis_max_rr,

            "range_cast": range_cast,
            "dice1": dice1,
            "dice2": dice2,
            "dice3": dice3,
            "dice4": dice4,
            "dice5": dice5,
            "miscast": miscast

        }
        return render(request, "tables.html", ctx)


class ParingsView(View):
    def get(self, request):
        parings_3_list = Parings_3.objects.all().order_by("-date")
        parings_4_list = Parings_4.objects.all().order_by("-date")
        parings_5_list = Parings_5.objects.all().order_by("-date")
        ctx = {
            "parings_3_list": parings_3_list,
            "parings_4_list": parings_4_list,
            "parings_5_list": parings_5_list,
        }
        return render(request, "parings_list.html", ctx)
    def post(self, request):
        pass


class ParingDetails3View(View):
    def get(self, request, id):
        result = []
        data_list = []
        points = []
        mp = []
        player = Parings_3.objects.get(pk=id)
        teamA = [player.p1, player.p2, player.p3]
        teamB = [player.op1, player.op2, player.op3]
        # request.session['teamA3'] = teamA
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (player.p1, player.op1):
                    i = player.p11
                elif i == (player.p2, player.op2):
                    i = player.p22
                elif i == (player.p3, player.op3):
                    i = player.p33
                elif i == (player.p1, player.op2):
                    i = player.p12
                elif i == (player.p1, player.op3):
                    i = player.p13
                elif i == (player.p2, player.op1):
                    i = player.p21
                elif i == (player.p2, player.op3):
                    i = player.p23
                elif i == (player.p3, player.op1):
                    i = player.p31
                elif i == (player.p3, player.op2):
                    i = player.p32
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        ctx = {
            "paring": player,
            "data_list": sorted_list
        }
        return render(request, "paring_details_3.html", ctx)


class AddParing3View(View):
    def get(self, request):
        # if request.session["teamA3"]:
        #     teamA = request.session['teamA3']
        #     form = ParingsForm(initial={
        #         "p1": teamA[0],
        #         "p2": teamA[1],
        #         "p3": teamA[2],
        #     })
        #     ctx = {"form": form}
        #     return render(request, "add_paring_3_form.html", ctx)
        # else:
        form = ParingsForm()
        ctx = {"form": form}
        return render(request, "add_paring_3_form.html", ctx)
    def post(self, request):
        form = ParingsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parings-view")


class EditParing3View(View):
    def get(self, request, id):
        paring = Parings_3.objects.get(pk=id)
        form = ParingsForm(instance=paring)
        ctx = {"form": form}
        return render(request, "add_paring_3_form.html", ctx)
    def post(self, request, id):
        paring = Parings_3.objects.get(pk=id)
        form = ParingsForm(request.POST, instance=paring)
        if form.is_valid():
            form.save()
            return redirect("paring-details-3", id=id)


class DeleteParing3View(View):
    def get(self, request, id):
        paring = Parings_3.objects.get(pk=id)
        paring.delete()
        return redirect("parings-view")


class ParingDetails4View(View):
    def get(self, request, id):
        result = []
        data_list = []
        points = []
        mp = []
        player = Parings_4.objects.get(pk=id)
        teamA = [player.p1, player.p2, player.p3, player.p4]
        teamB = [player.op1, player.op2, player.op3, player.op4]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (player.p1, player.op1):
                    i = player.p11
                elif i == (player.p1, player.op2):
                    i = player.p12
                elif i == (player.p1, player.op3):
                    i = player.p13
                elif i == (player.p1, player.op4):
                    i = player.p14
                elif i == (player.p2, player.op1):
                    i = player.p21
                elif i == (player.p2, player.op2):
                    i = player.p22
                elif i == (player.p2, player.op3):
                    i = player.p23
                elif i == (player.p2, player.op4):
                    i = player.p24
                elif i == (player.p3, player.op1):
                    i = player.p31
                elif i == (player.p3, player.op2):
                    i = player.p32
                elif i == (player.p3, player.op3):
                    i = player.p33
                elif i == (player.p3, player.op4):
                    i = player.p34
                elif i == (player.p4, player.op1):
                    i = player.p41
                elif i == (player.p4, player.op2):
                    i = player.p42
                elif i == (player.p4, player.op3):
                    i = player.p43
                elif i == (player.p4, player.op4):
                    i = player.p44
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        form = FirstParingsForm()
        ctx = {
            "paring": player,
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "form": form
        }
        return render(request, "paring_details_4.html", ctx)


class AddParing4View(View):
    def get(self, request):
        form = Parings4Form()
        ctx = {"form": form}
        return render(request, "add_paring_4_form.html", ctx)
    def post(self, request):
        form = Parings4Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parings-view")


class EditParing4View(View):
    def get(self, request, id):
        paring = Parings_4.objects.get(pk=id)
        form = Parings4Form(instance=paring)
        ctx = {"form": form}
        return render(request, "add_paring_4_form.html", ctx)
    def post(self, request, id):
        paring = Parings_4.objects.get(pk=id)
        form = Parings4Form(request.POST, instance=paring)
        if form.is_valid():
            form.save()
            return redirect("paring-details-4", id=id)


class DeleteParing4View(View):
    def get(self, request, id):
        paring = Parings_4.objects.get(pk=id)
        paring.delete()
        return redirect("parings-view")



class ParingDetails5View(View):
    def get(self, request, id):
        result = []
        data_list = []
        points = []
        mp = []
        player = Parings_5.objects.get(pk=id)
        teamA = [player.p1, player.p2, player.p3, player.p4, player.p5]
        teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (player.p1, player.op1):
                    i = player.p11
                elif i == (player.p1, player.op2):
                    i = player.p12
                elif i == (player.p1, player.op3):
                    i = player.p13
                elif i == (player.p1, player.op4):
                    i = player.p14
                elif i == (player.p1, player.op5):
                    i = player.p15
                elif i == (player.p2, player.op1):
                    i = player.p21
                elif i == (player.p2, player.op2):
                    i = player.p22
                elif i == (player.p2, player.op3):
                    i = player.p23
                elif i == (player.p2, player.op4):
                    i = player.p24
                elif i == (player.p2, player.op5):
                    i = player.p25
                elif i == (player.p3, player.op1):
                    i = player.p31
                elif i == (player.p3, player.op2):
                    i = player.p32
                elif i == (player.p3, player.op3):
                    i = player.p33
                elif i == (player.p3, player.op4):
                    i = player.p34
                elif i == (player.p3, player.op5):
                    i = player.p35
                elif i == (player.p4, player.op1):
                    i = player.p41
                elif i == (player.p4, player.op2):
                    i = player.p42
                elif i == (player.p4, player.op3):
                    i = player.p43
                elif i == (player.p4, player.op4):
                    i = player.p44
                elif i == (player.p4, player.op5):
                    i = player.p45
                elif i == (player.p5, player.op1):
                    i = player.p51
                elif i == (player.p5, player.op2):
                    i = player.p52
                elif i == (player.p5, player.op3):
                    i = player.p53
                elif i == (player.p5, player.op4):
                    i = player.p54
                elif i == (player.p5, player.op5):
                    i = player.p55
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        form = FirstParingsForm()
        ctx = {
            "paring": player,
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "form": form
        }
        return render(request, "paring_details_5.html", ctx)
    def post(self, request, id):
        form = FirstParingsForm(request.POST)
        if form.is_valid():
            first_p1 = form.cleaned_data["first_p1"].short_name
            first_op1 = form.cleaned_data["first_op1"].short_name
            first_p2 = form.cleaned_data["first_p2"].short_name
            first_op2 = form.cleaned_data["first_op2"].short_name
            result = []
            data_list = []
            points = []
            mp = []
            player = Parings_5.objects.get(pk=id)
            teamA = [player.p1, player.p2, player.p3, player.p4, player.p5]
            teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
            for perm in permutations(teamA):
                result.append(list(zip(perm, teamB)))
            for pairing in result:
                score = []
                total = 0
                for i in pairing:
                    if i == (player.p1, player.op1):
                        i = player.p11
                    elif i == (player.p1, player.op2):
                        i = player.p12
                    elif i == (player.p1, player.op3):
                        i = player.p13
                    elif i == (player.p1, player.op4):
                        i = player.p14
                    elif i == (player.p1, player.op5):
                        i = player.p15
                    elif i == (player.p2, player.op1):
                        i = player.p21
                    elif i == (player.p2, player.op2):
                        i = player.p22
                    elif i == (player.p2, player.op3):
                        i = player.p23
                    elif i == (player.p2, player.op4):
                        i = player.p24
                    elif i == (player.p2, player.op5):
                        i = player.p25
                    elif i == (player.p3, player.op1):
                        i = player.p31
                    elif i == (player.p3, player.op2):
                        i = player.p32
                    elif i == (player.p3, player.op3):
                        i = player.p33
                    elif i == (player.p3, player.op4):
                        i = player.p34
                    elif i == (player.p3, player.op5):
                        i = player.p35
                    elif i == (player.p4, player.op1):
                        i = player.p41
                    elif i == (player.p4, player.op2):
                        i = player.p42
                    elif i == (player.p4, player.op3):
                        i = player.p43
                    elif i == (player.p4, player.op4):
                        i = player.p44
                    elif i == (player.p4, player.op5):
                        i = player.p45
                    elif i == (player.p5, player.op1):
                        i = player.p51
                    elif i == (player.p5, player.op2):
                        i = player.p52
                    elif i == (player.p5, player.op3):
                        i = player.p53
                    elif i == (player.p5, player.op4):
                        i = player.p54
                    elif i == (player.p5, player.op5):
                        i = player.p55
                    points.append(i)
                    for s in points:
                        if s == -2:
                            mp = 3
                        elif s == -1:
                            mp = 7
                        elif s == 1:
                            mp = 13
                        elif s == 2:
                            mp = 17
                        else:
                            mp = 10
                    score.append(mp)
                    total += mp
                data_list.append([pairing, score, total])
            sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
            filtered_list = []
            pre_list = []
            for i in range(len(data_list)-1):
                for j in range(5):
                    if data_list[i][0][j] == (first_p1, first_op1):
                        pre_list.append(data_list[i])
            for i in range(len(pre_list)-1):
                for j in range(5):
                    if pre_list[i][0][j] == (first_p2, first_op2):
                        filtered_list.append(pre_list[i])
            sorted_filtered_list = sorted(filtered_list, key=itemgetter(2), reverse=True)
            ctx = {
                "paring": player,
                "data_list": sorted_list[:6],
                "data_list_bad": sorted_list[-6:],
                "filtered_list": sorted_filtered_list,
                "first_p1": first_p1,
                "first_p2": first_p2
            }
            return render(request, "paring_details_5.html", ctx)


class EditParing5View(View):
    def get(self, request, id):
        paring = Parings_5.objects.get(pk=id)
        form = Parings5Form(instance=paring)
        ctx = {"form": form}
        return render(request, "add_paring_5_form.html", ctx)
    def post(self, request, id):
        paring = Parings_5.objects.get(pk=id)
        form = Parings5Form(request.POST, instance=paring)
        if form.is_valid():
            form.save()
            return redirect("paring-details-5", id=id)


class AddParing5View(View):
    def get(self, request):
        form = Parings5Form()
        ctx = {"form": form}
        return render(request, "add_paring_5_form.html", ctx)
    def post(self, request):
        form = Parings5Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect("parings-view")


class DeleteParing5View(View):
    def get(self, request, id):
        paring = Parings_5.objects.get(pk=id)
        paring.delete()
        return redirect("parings-view")


class TournamentsView(View):
    def get(self, request):
        tournaments_list = Tournaments.objects.all().order_by("-date")
        ctx = {
            "tournaments_list": tournaments_list,
        }

        return render(request, "tournaments_list.html", ctx)


class AddTournamentView(View):
    def get(self, request):
        form = TournamentsForm(initial={"date": datetime.now()})
        ctx = {"form": form}
        return render(request, "add_tournament_form.html", ctx)
    def post(self, request):
        form = TournamentsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("tournaments-view")


class EditTournamentView(View):
    def get(self, request, id):
        tournament = Tournaments.objects.get(pk=id)
        form = TournamentsForm(instance=tournament)
        ctx = {"form": form}
        return render(request, "add_tournament_form.html", ctx)
    def post(self, request, id):
        tournament = Tournaments.objects.get(pk=id)
        form = TournamentsForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect("tournaments-view")


class DeleteTournamentView(View):
    def get(self, request, id):
        t = Tournaments.objects.get(pk=id)
        t.delete()
        return redirect("tournaments-view")


class TournamentParingsView(View):
    def get(self, request, id):
        tournament = Tournaments.objects.get(pk=id)
        parings_list = Team_of_3.objects.filter(tournament=tournament.id).order_by("name")
        parings_list2 = Team_of_4.objects.filter(tournament=tournament.id).order_by("name")
        parings_list3 = Team_of_5.objects.filter(tournament=tournament.id).order_by("name")
        form = TParings3Form()
        form2 = TParings4Form()
        form3 = TParings5Form()
        if tournament.no_of_players == 3:
            ctx = {
                "tournament": tournament,
                "parings_list": parings_list,
                "form": form
            }
            return render(request, "tournament_parings_3.html", ctx)
        elif tournament.no_of_players == 4:
            ctx = {
                "tournament": tournament,
                "parings_list": parings_list2,
                "form": form2
            }
            return render(request, "tournament_parings_4.html", ctx)
        elif tournament.no_of_players == 5:
            ctx = {
                "tournament": tournament,
                "parings_list": parings_list3,
                "form": form3
            }
            return render(request, "tournament_parings_5.html", ctx)
    def post(self, request, id):
        tournament = Tournaments.objects.get(pk=id)
        if tournament.no_of_players == 3:
            form = TParings3Form(request.POST)
            if form.is_valid():
                result = form.save(commit=False)
                result.tournament = tournament
                result.save()
                return redirect("tournament-parings", id=id)
        elif tournament.no_of_players == 4:
            form = TParings4Form(request.POST)
            if form.is_valid():
                result = form.save(commit=False)
                result.tournament = tournament
                result.save()
                return redirect("tournament-parings", id=id)
        elif tournament.no_of_players == 5:
            form = TParings5Form(request.POST)
            if form.is_valid():
                result = form.save(commit=False)
                result.tournament = tournament
                result.save()
                return redirect("tournament-parings", id=id)


class TParing3v3View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_3.objects.get(pk=par)
        result = []
        data_list = []
        points = []
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3]
        teamB = [player.op1, player.op2, player.op3]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (tournament.p1, player.op1):
                    i = player.p11
                elif i == (tournament.p1, player.op2):
                    i = player.p12
                elif i == (tournament.p1, player.op3):
                    i = player.p13
                elif i == (tournament.p2, player.op1):
                    i = player.p21
                elif i == (tournament.p2, player.op2):
                    i = player.p22
                elif i == (tournament.p2, player.op3):
                    i = player.p23
                elif i == (tournament.p3, player.op1):
                    i = player.p31
                elif i == (tournament.p3, player.op2):
                    i = player.p32
                elif i == (tournament.p3, player.op3):
                    i = player.p33
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        ctx = {
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,

        }
        return render(request, "paring_3v3.html", ctx)


class TParing4v4View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_4.objects.get(pk=par)
        result = []
        data_list = []
        points = []
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4]
        teamB = [player.op1, player.op2, player.op3, player.op4]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (tournament.p1, player.op1):
                    i = player.p11
                elif i == (tournament.p1, player.op2):
                    i = player.p12
                elif i == (tournament.p1, player.op3):
                    i = player.p13
                elif i == (tournament.p1, player.op4):
                    i = player.p14
                elif i == (tournament.p2, player.op1):
                    i = player.p21
                elif i == (tournament.p2, player.op2):
                    i = player.p22
                elif i == (tournament.p2, player.op3):
                    i = player.p23
                elif i == (tournament.p2, player.op4):
                    i = player.p24
                elif i == (tournament.p3, player.op1):
                    i = player.p31
                elif i == (tournament.p3, player.op2):
                    i = player.p32
                elif i == (tournament.p3, player.op3):
                    i = player.p33
                elif i == (tournament.p3, player.op4):
                    i = player.p34
                elif i == (tournament.p4, player.op1):
                    i = player.p41
                elif i == (tournament.p4, player.op2):
                    i = player.p42
                elif i == (tournament.p4, player.op3):
                    i = player.p43
                elif i == (tournament.p4, player.op4):
                    i = player.p44
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        ctx = {
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,
        }
        return render(request, "paring_4v4.html", ctx)


class TParing5v5View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_5.objects.get(pk=par)
        result = []
        data_list = []
        points = []
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4, tournament.p5]
        teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                if i == (tournament.p1, player.op1):
                    i = player.p11
                elif i == (tournament.p1, player.op2):
                    i = player.p12
                elif i == (tournament.p1, player.op3):
                    i = player.p13
                elif i == (tournament.p1, player.op4):
                    i = player.p14
                elif i == (tournament.p1, player.op5):
                    i = player.p15
                elif i == (tournament.p2, player.op1):
                    i = player.p21
                elif i == (tournament.p2, player.op2):
                    i = player.p22
                elif i == (tournament.p2, player.op3):
                    i = player.p23
                elif i == (tournament.p2, player.op4):
                    i = player.p24
                elif i == (tournament.p2, player.op5):
                    i = player.p25
                elif i == (tournament.p3, player.op1):
                    i = player.p31
                elif i == (tournament.p3, player.op2):
                    i = player.p32
                elif i == (tournament.p3, player.op3):
                    i = player.p33
                elif i == (tournament.p3, player.op4):
                    i = player.p34
                elif i == (tournament.p3, player.op5):
                    i = player.p35
                elif i == (tournament.p4, player.op1):
                    i = player.p41
                elif i == (tournament.p4, player.op2):
                    i = player.p42
                elif i == (tournament.p4, player.op3):
                    i = player.p43
                elif i == (tournament.p4, player.op4):
                    i = player.p44
                elif i == (tournament.p4, player.op5):
                    i = player.p45
                elif i == (tournament.p5, player.op1):
                    i = player.p51
                elif i == (tournament.p5, player.op2):
                    i = player.p52
                elif i == (tournament.p5, player.op3):
                    i = player.p53
                elif i == (tournament.p5, player.op4):
                    i = player.p54
                elif i == (tournament.p5, player.op5):
                    i = player.p55
                points.append(i)
                for s in points:
                    if s == -2:
                        mp = 3
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 17
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        form = FirstParingsForm()
        ctx = {
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,
            "form": form,
        }
        return render(request, "paring_5v5.html", ctx)

    def post(self, request, id, par):
        form = FirstParingsForm(request.POST)
        if form.is_valid():
            first_p1 = form.cleaned_data["first_p1"].short_name
            first_op1 = form.cleaned_data["first_op1"].short_name
            first_p2 = form.cleaned_data["first_p2"].short_name
            first_op2 = form.cleaned_data["first_op2"].short_name
            result = []
            data_list = []
            points = []
            mp = []
            tournament = Tournaments.objects.get(pk=id)
            player = Team_of_5.objects.get(pk=par)
            teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4, tournament.p5]
            teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
            for perm in permutations(teamA):
                result.append(list(zip(perm, teamB)))
            for pairing in result:
                score = []
                total = 0
                for i in pairing:
                    if i == (tournament.p1, player.op1):
                        i = player.p11
                    elif i == (tournament.p1, player.op2):
                        i = player.p12
                    elif i == (tournament.p1, player.op3):
                        i = player.p13
                    elif i == (tournament.p1, player.op4):
                        i = player.p14
                    elif i == (tournament.p1, player.op5):
                        i = player.p15
                    elif i == (tournament.p2, player.op1):
                        i = player.p21
                    elif i == (tournament.p2, player.op2):
                        i = player.p22
                    elif i == (tournament.p2, player.op3):
                        i = player.p23
                    elif i == (tournament.p2, player.op4):
                        i = player.p24
                    elif i == (tournament.p2, player.op5):
                        i = player.p25
                    elif i == (tournament.p3, player.op1):
                        i = player.p31
                    elif i == (tournament.p3, player.op2):
                        i = player.p32
                    elif i == (tournament.p3, player.op3):
                        i = player.p33
                    elif i == (tournament.p3, player.op4):
                        i = player.p34
                    elif i == (tournament.p3, player.op5):
                        i = player.p35
                    elif i == (tournament.p4, player.op1):
                        i = player.p41
                    elif i == (tournament.p4, player.op2):
                        i = player.p42
                    elif i == (tournament.p4, player.op3):
                        i = player.p43
                    elif i == (tournament.p4, player.op4):
                        i = player.p44
                    elif i == (tournament.p4, player.op5):
                        i = player.p45
                    elif i == (tournament.p5, player.op1):
                        i = player.p51
                    elif i == (tournament.p5, player.op2):
                        i = player.p52
                    elif i == (tournament.p5, player.op3):
                        i = player.p53
                    elif i == (tournament.p5, player.op4):
                        i = player.p54
                    elif i == (tournament.p5, player.op5):
                        i = player.p55
                    points.append(i)
                    for s in points:
                        if s == -2:
                            mp = 3
                        elif s == -1:
                            mp = 7
                        elif s == 1:
                            mp = 13
                        elif s == 2:
                            mp = 17
                        else:
                            mp = 10
                    score.append(mp)
                    total += mp
                data_list.append([pairing, score, total])
            sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
            filtered_list = []
            pre_list = []
            for i in range(len(data_list)-1):
                for j in range(5):
                    if data_list[i][0][j] == (first_p1, first_op1):
                        pre_list.append(data_list[i])
            for i in range(len(pre_list)-1):
                for j in range(5):
                    if pre_list[i][0][j] == (first_p2, first_op2):
                        filtered_list.append(pre_list[i])
            sorted_filtered_list = sorted(filtered_list, key=itemgetter(2), reverse=True)
            ctx = {
                "paring": player,
                "data_list": sorted_list[:6],
                "data_list_bad": sorted_list[-6:],
                "filtered_list": sorted_filtered_list,
                "first_p1": first_p1,
                "first_p2": first_p2
            }
            return render(request, "paring_5v5.html", ctx)


class EditTParing3v3View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        parings_list = Team_of_3.objects.filter(tournament=tournament.id).order_by("name")
        paring = Team_of_3.objects.get(pk=par)
        form = TParings3Form(instance=paring)
        ctx = {
            "tournament": tournament,
            "form": form,
            "parings_list": parings_list,
        }
        return render(request, "tournament_parings_3.html", ctx)

    def post(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        paring = Team_of_3.objects.get(pk=par)
        form = TParings3Form(request.POST, instance=paring)
        if form.is_valid():
            result = form.save(commit=False)
            result.tournament = tournament
            result.save()
            return redirect("paring-3v3-view", id=id, par=par)


class EditTParing4v4View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        parings_list = Team_of_4.objects.filter(tournament=tournament.id).order_by("name")
        paring = Team_of_4.objects.get(pk=par)
        form = TParings4Form(instance=paring)
        ctx = {
            "tournament": tournament,
            "form": form,
            "parings_list": parings_list,
        }
        return render(request, "tournament_parings_4.html", ctx)

    def post(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        paring = Team_of_4.objects.get(pk=par)
        form = TParings4Form(request.POST, instance=paring)
        if form.is_valid():
            result = form.save(commit=False)
            result.tournament = tournament
            result.save()
            return redirect("paring-4v4-view", id=id, par=par)


class EditTParing5v5View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        parings_list = Team_of_5.objects.filter(tournament=tournament.id).order_by("name")
        paring = Team_of_5.objects.get(pk=par)
        form = TParings5Form(instance=paring)
        ctx = {
            "tournament": tournament,
            "form": form,
            "parings_list": parings_list,
        }
        return render(request, "tournament_parings_5.html", ctx)

    def post(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        paring = Team_of_5.objects.get(pk=par)
        form = TParings5Form(request.POST, instance=paring)
        if form.is_valid():
            result = form.save(commit=False)
            result.tournament = tournament
            result.save()
            return redirect("paring-5v5-view", id=id, par=par)


class DeleteTParing3v3View(View):
    def get(self, request, id, par):
        p = Team_of_3.objects.get(pk=par)
        p.delete()
        return redirect("tournament-parings", id=id)


class DeleteTParing4v4View(View):
    def get(self, request, id, par):
        p = Team_of_4.objects.get(pk=par)
        p.delete()
        return redirect("tournament-parings", id=id)


class DeleteTParing5v5View(View):
    def get(self, request, id, par):
        p = Team_of_5.objects.get(pk=par)
        p.delete()
        return redirect("tournament-parings", id=id)


class ArmyIconsView(View):
    def get(self, request):
        form = ArmyIconForm()
        ctx = {"form": form}
        return render(request, "paring_icons.html", ctx)

    def post(selfself, request):
        army_list = Armys.objects.all().order_by("name")
        form = ArmyIconForm(request.POST)
        if form.is_valid():
            army1 = form.cleaned_data["army1"]
            army2 = form.cleaned_data["army2"]
            icon1 = Armys.objects.get(name=army1)
            if army2:
                icon2 = Armys.objects.get(name=army2)
                ctx = {
                    "army_list": army_list,
                    "icon1": icon1,
                    "icon2": icon2,
                }
            else:
                ctx = {
                    "army_list": army_list,
                    "icon1": icon1,
                }
        return render(request, "paring_icons.html", ctx)
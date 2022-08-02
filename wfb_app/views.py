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
    DiceRollForm, FirstParingsForm, TournamentsForm, TParings3Form, \
    TParings4Form, TParings5Form, ArmyIconForm, ETCForm, TParings8Form
from wfb_app.models import Units, Armys, GameResults, Profile, Tournaments, Team_of_3, \
    Team_of_4, Team_of_5, TournamentETC, Team_of_8
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Avg, Max, Min, Sum
import random

MAX_GAMES = [100, 100, 200]
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
    def get(self, request):
        result_master = []
        result_local = []
        result_home = []
        users = User.objects.all().exclude(username="admin")
        no_of_games = GAMES_YEAR.count()
        for user in users:
            wins = 0
            losses = 0
            draws = 0
            games = GAMES_YEAR.filter(user=user)
            master = games.filter(game_rank="master")
            local = games.filter(game_rank="local")
            home = games.filter(game_rank="home")
            count_masters = master.count()
            count_locals = local.count()
            count_homes = home.count()
            total_masters = master.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            total_locals = local.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            total_homes = home.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
            for record in master:
                if record.battle_points > 10:
                    wins += 1
                elif record.battle_points < 10:
                    losses += 1
                elif record.battle_points == 10:
                    draws += 1
            d = wins+losses
            if d > 0:
                win_rate = round(wins / d * 100, 1)
            else:
                win_rate = 0.0
            result_master.append([total_masters, user.id, user, win_rate, wins, losses, draws,  count_masters])
            wins = 0
            losses = 0
            draws = 0
            for record in local:
                if record.battle_points > 10:
                    wins += 1
                elif record.battle_points < 10:
                    losses += 1
                elif record.battle_points == 10:
                    draws += 1
            d = wins+losses
            if d > 0:
                win_rate = round(wins / d * 100, 1)
            else:
                win_rate = 0.0
            result_local.append([total_locals, user.id, user, win_rate, wins, losses, draws,  count_locals])
            wins = 0
            losses = 0
            draws = 0
            for record in home:
                if record.battle_points > 10:
                    wins += 1
                elif record.battle_points < 10:
                    losses += 1
                elif record.battle_points == 10:
                    draws += 1
            d = wins + losses
            if d > 0:
                win_rate = round(wins / d * 100, 1)
            else:
                win_rate = 0.0
            result_home.append([total_homes, user.id, user, win_rate, wins, losses, draws, count_homes])

        result_master.sort(reverse=True)
        result_local.sort(reverse=True)
        result_home.sort(reverse=True)
        ctx = {
            "no_of_users": users.count(),
            "no_of_games": no_of_games,
            "result_master": result_master,
            "result_local": result_local,
            "result_home": result_home,

        }
        return render(request, "index2.html", ctx)

    def post(self, request):
        pass


# class Index(View):
#     # strona główna, 5ciu najleprzysz graczy, logowanie, linki
#     def get(self, request):
#         result = []
#         users = User.objects.all().exclude(username="admin")
#         no_of_games = GAMES_YEAR.count()
#         max = MAX_GAMES
#         for user in users:
#             games = GAMES_YEAR.filter(user=user)
#             master = games.filter(game_rank="master")
#             local = games.filter(game_rank="local")
#             home = games.filter(game_rank="home")
#             count_master = master.count()
#             count_local = local.count()
#             count_home = home.count()
#             total_masters = master.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             total_locals = local.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             total_homes = home.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             best_masters = master.order_by("-battle_points")[:max[0]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             best_locals = local.order_by("-battle_points")[:max[1]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             best_homes = home.order_by("-battle_points")[:max[2]].aggregate(Sum("battle_points"))['battle_points__sum'] or 0
#             if count_master == 0:
#                 av_master = 0
#             else:
#                 av_master = round(total_masters / count_master, 1)
#             if count_local == 0:
#                 av_local = 0
#             else:
#                 av_local = round(total_locals / count_local, 1)
#             if count_home == 0:
#                 av_home = 0
#             else:
#                 av_home = round(total_homes / count_home, 1)
#
#             total = total_masters + total_locals + total_homes
#             count = count_master + count_local + count_home
#             ranking_points = best_masters + best_locals + best_homes
#             result.append([
#                 ranking_points,
#                 total,
#                 count,
#                 best_masters,
#                 total_masters,
#                 count_master,
#                 av_master,
#
#                 best_locals,
#                 total_locals,
#                 count_local,
#                 av_local,
#
#                 best_homes,
#                 total_homes,
#                 count_home,
#                 av_home,
#                 user.id,
#                 user,
#             ])
#         result.sort(reverse=True)
#         result_by_count = sorted(result)
#         result_by_count.sort(key=sort_count, reverse=True)
#         # result_by_rv = sorted(result)
#         # result_by_rv.sort(key=sort_rv, reverse=True)
#         ctx = {
#             "no_of_users": users.count(),
#             "no_of_games": no_of_games,
#             "result": result,
#             "best_gen_id": result[0][15],
#             "best_gamer_id": result_by_count[0][15],
#             "best_veg_id": result[-1][15],
#             "max": max
#         }
#         return render(request, "index.html", ctx)


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
        master = ranking.filter(game_rank="master")
        local = ranking.filter(game_rank="local")
        home = ranking.filter(game_rank="home")
        count_master = master.count()
        count_local = local.count()
        count_home = home.count()
        count_all = ranking.count()
        total_masters = master.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
        total_locals = local.aggregate(Sum("battle_points"))['battle_points__sum'] or 0
        total_homes = home.aggregate(Sum("battle_points"))['battle_points__sum'] or 0

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
        for score in ranking:
            total += score.battle_points
        data = [
            count_master,
            total_masters,
            av_master,
            count_local,
            total_locals,
            av_local,
            count_home,
            total_homes,
            av_home,
            count_all]

        ctx = {
            "ranking": ranking,
            "total": total,
            "user": user,
            "data": data,
        }
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
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="master").order_by("-date", "-id")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="local").order_by("-date", "-id")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GAMES_YEAR.filter(user=user).filter(game_rank="home").order_by("-date", "-id")[:MAX_GAMES[2]]

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
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="master").order_by("-date", "-id")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="local").order_by("-date", "-id")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GameResults.objects.filter(date__year=2021).filter(user=user).filter(game_rank="home").order_by("-date", "-id")[:MAX_GAMES[2]]

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
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="master").order_by("-date", "-id")[:MAX_GAMES[0]]
        elif request.method == "POST" and "best_locals" in request.POST:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="local").order_by("-date", "-id")[:MAX_GAMES[1]]
        elif request.method == "POST" and "best_homes" in request.POST:
            ranking = GameResults.objects.filter(date__year=2020).filter(user=user).filter(game_rank="home").order_by("-date", "-id")[:MAX_GAMES[2]]

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
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3]
        teamB = [player.op1, player.op2, player.op3]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                points = []
                for A in teamA:
                    for B in teamB:
                        if i == (A, B):
                            x = teamA.index(A) + 1
                            y = teamB.index(B) + 1
                            attr = f"p{x}{y}"
                            j = getattr(player, attr)
                            # i = player.p11 ...
                        points.append(j)
                for s in points:
                    if s == -3:
                        mp = 1
                    elif s == -2:
                        mp = 4
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 16
                    elif s == 3:
                        mp = 19
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        green = 0
        yellow = 0
        red = 0
        for i in sorted_list:
            if i[2] > 41:
                green += 1
            elif i[2] < 39:
                red += 1
            else:
                yellow += 1
        total = green + yellow + red
        green_p = green / total * 100
        yellow_p = yellow / total * 100
        red_p = red / total * 100
        ctx = {
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_p": green_p,
            "yellow_p": yellow_p,
            "red_p": red_p,

        }
        return render(request, "paring_3v3.html", ctx)


class TParing4v4View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_4.objects.get(pk=par)
        result = []
        data_list = []
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4]
        teamB = [player.op1, player.op2, player.op3, player.op4]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                points = []
                for A in teamA:
                    for B in teamB:
                        if i == (A, B):
                            x = teamA.index(A) + 1
                            y = teamB.index(B) + 1
                            attr = f"p{x}{y}"
                            j = getattr(player, attr)
                            # i = player.p11 ...
                        points.append(j)
                for s in points:
                    if s == -3:
                        mp = 1
                    elif s == -2:
                        mp = 4
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 16
                    elif s == 3:
                        mp = 19
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        green = 0
        yellow = 0
        red = 0
        for i in sorted_list:
            if i[2] > 41:
                green += 1
            elif i[2] < 39:
                red += 1
            else:
                yellow += 1
        total = green + yellow + red
        green_p = green / total * 100
        yellow_p = yellow / total * 100
        red_p = red / total * 100
        ctx = {
            "data_list": sorted_list,
            # "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_p": green_p,
            "yellow_p": yellow_p,
            "red_p": red_p,
        }
        return render(request, "paring_4v4.html", ctx)


class TParing5v5View(View):
    def get(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_5.objects.get(pk=par)
        form = FirstParingsForm()
        result = []
        data_list = []
        mp = []
        teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4, tournament.p5]
        teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            score = []
            total = 0
            for i in pairing:
                points = []
                for A in teamA:
                    for B in teamB:
                        if i == (A, B):
                            x = teamA.index(A) + 1
                            y = teamB.index(B) + 1
                            attr = f"p{x}{y}"
                            j = getattr(player, attr)
                            # i = player.p11 ...
                        points.append(j)
                for s in points:
                    if s == -3:
                        mp = 1
                    elif s == -2:
                        mp = 4
                    elif s == -1:
                        mp = 7
                    elif s == 1:
                        mp = 13
                    elif s == 2:
                        mp = 16
                    elif s == 3:
                        mp = 19
                    else:
                        mp = 10
                score.append(mp)
                total += mp
            data_list.append([pairing, score, total])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        green = 0
        yellow = 0
        red = 0
        for i in sorted_list:
            if i[2] > 51:
                green += 1
            elif i[2] < 49:
                red += 1
            else:
                yellow += 1
        total = green + yellow + red
        green_p = green / total * 100
        yellow_p = yellow / total * 100
        red_p = red / total * 100
        ctx = {
            "data_list": sorted_list[:6],
            "data_list_bad": sorted_list[-6:],
            "tournament": tournament,
            "paring": player,
            "form": form,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_p": green_p,
            "yellow_p": yellow_p,
            "red_p": red_p,
        }
        return render(request, "paring_5v5.html", ctx)

    def post(self, request, id, par):
        tournament = Tournaments.objects.get(pk=id)
        player = Team_of_5.objects.get(pk=par)
        form = FirstParingsForm(request.POST)
        if form.is_valid():
            first_p1 = form.cleaned_data["first_p1"].short_name
            first_op1 = form.cleaned_data["first_op1"].short_name
            first_p2 = form.cleaned_data["first_p2"].short_name
            first_op2 = form.cleaned_data["first_op2"].short_name
            result = []
            data_list = []
            mp = []
            teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4, tournament.p5]
            teamB = [player.op1, player.op2, player.op3, player.op4, player.op5]
            for perm in permutations(teamA):
                result.append(list(zip(perm, teamB)))
            for pairing in result:
                score = []
                total = 0
                for i in pairing:
                    points = []
                    for A in teamA:
                        for B in teamB:
                            if i == (A, B):
                                x = teamA.index(A) + 1
                                y = teamB.index(B) + 1
                                attr = f"p{x}{y}"
                                j = getattr(player, attr)
                                # i = player.p11 ...
                            points.append(j)
                    for s in points:
                        if s == -3:
                            mp = 1
                        elif s == -2:
                            mp = 4
                        elif s == -1:
                            mp = 7
                        elif s == 1:
                            mp = 13
                        elif s == 2:
                            mp = 16
                        elif s == 3:
                            mp = 19
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
            next_paring = []
            for i in range(len(sorted_filtered_list)-1):
                for j in range(5):
                    if sorted_filtered_list[i][1][j] > 10:
                        next_paring.append(sorted_filtered_list[i][0][j][0])
            rating = dict((i, next_paring.count(i)) for i in next_paring)
            if first_p1 in rating:
                del rating[first_p1]
            if first_p2 in rating:
                del rating[first_p2]
            green = 0
            yellow = 0
            red = 0
            for i in sorted_filtered_list:
                if i[2] > 51:
                    green += 1
                elif i[2] < 49:
                    red += 1
                else:
                    yellow += 1
            total = green + yellow + red
            green_p = green / total * 100
            yellow_p = yellow / total * 100
            red_p = red / total * 100
            ctx = {
                "paring": player,
                "tournament": tournament,
                "data_list": sorted_list[:6],
                "data_list_bad": sorted_list[-6:],
                "filtered_list": sorted_filtered_list,
                "first_p1": first_p1,
                "first_p2": first_p2,
                "green": green,
                "yellow": yellow,
                "red": red,
                "green_p": green_p,
                "yellow_p": yellow_p,
                "red_p": red_p,
                "best_armies": rating,
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

class TournamentETCView(View):
    def get(self, request):
        tournaments_list = TournamentETC.objects.all().order_by("-date")
        ctx = {
            "tournaments_list": tournaments_list,
        }
        return render(request, "etc_list.html", ctx)


class AddTournamentETCView(View):
    def get(self, request):
        form = ETCForm(initial={"date": datetime.now()})
        ctx = {"form": form}
        return render(request, "add_etc_form.html", ctx)
    def post(self, request):
        form = ETCForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("etc-view")

class EditTournamentETCView(View):
    def get(self, request, id):
        tournament = TournamentETC.objects.get(pk=id)
        form = ETCForm(instance=tournament)
        ctx = {"form": form}
        return render(request, "add_etc_form.html", ctx)
    def post(self, request, id):
        tournament = TournamentETC.objects.get(pk=id)
        form = ETCForm(request.POST, instance=tournament)
        if form.is_valid():
            form.save()
            return redirect("etc-view")


class DeleteTournamentETCView(View):
    def get(self, request, id):
        t = TournamentETC.objects.get(pk=id)
        t.delete()
        return redirect("tournaments-view")


class ETCParingsView(View):
    def get(self, request, id):
        tournament = TournamentETC.objects.get(pk=id)
        parings_list = Team_of_8.objects.filter(tournament=tournament.id).order_by("name")
        form = TParings8Form()
        ctx = {
            "tournament": tournament,
            "parings_list": parings_list,
            "form": form
            }
        return render(request, "etc_parings.html", ctx)

    def post(self, request, id):
        tournament = TournamentETC.objects.get(pk=id)
        form = TParings8Form(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.tournament = tournament
            result.save()
            return redirect("etc-parings", id=id)


class TParing8v8View(View):
    def get(self, request, id, par):
        tournament = TournamentETC.objects.get(pk=id)
        player = Team_of_8.objects.get(pk=par)
        form = FirstParingsForm()
        result = []
        data_list = []
        players_points = []
        army_points = []
        for w in range(1, 9):
            p1points = []
            attr2 = f'player_name_{w}'
            attr3 = f'p{w}'
            for z in range(1, 9):
                attr1 = f'p{w}{z}'
                j1 = getattr(player, attr1)
                p1points.append(j1)
            av1 = round(sum(p1points) / 8, 2)
            p1points.append(av1)
            player_name = getattr(tournament, attr2)
            player_army = getattr(tournament, attr3)
            player_data = player_name, player_army
            player_p = p1points, player_data
            players_points.append(player_p)
        for w in range(1, 9):
            p2points = []
            for z in range(1, 9):
                attr2 = f'p{z}{w}'
                j2 = getattr(player, attr2)
                p2points.append(j2)
            av2 = round(sum(p2points) / 8, 2)
            army_points.append(av2)
        teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4,
                 tournament.p5, tournament.p6, tournament.p7, tournament.p8]
        teamB = [player.op1, player.op2, player.op3, player.op4,
                 player.op5, player.op6, player.op7, player.op8]
        for perm in permutations(teamA):
            result.append(list(zip(perm, teamB)))
        for pairing in result:
            total = 0
            for i in pairing:
                for A in teamA:
                    for B in teamB:
                        if i == (A, B):
                            x = teamA.index(A) + 1
                            y = teamB.index(B) + 1
                            attr = f"p{x}{y}"
                            j = getattr(player, attr)
                            # j = player.p11 ...
                total += j
                average = total / 8
            data_list.append([pairing, total, average])
        sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
        green = 0
        yellow = 0
        red = 0
        for i in sorted_list:
            if i[2] > 0:
                green += 1
            elif i[2] < 0:
                red += 1
            else:
                yellow += 1
        total = green + yellow + red
        green_p = green / total * 100
        yellow_p = yellow / total * 100
        red_p = red / total * 100
        total_percentage = []
        for A in teamA:
            percentage_of_paring = []
            for B in teamB:
                hipotetical_list = []
                for i in range(len(data_list) - 1):
                    for j in range(8):
                        if data_list[i][0][j] == (A, B):
                            hipotetical_list.append(data_list[i])
                green2 = 0
                yellow2 = 0
                red2 = 0
                for i in hipotetical_list:
                    if i[2] > 0:
                        green2 += 1
                    elif i[2] < 0:
                        red2 += 1
                    else:
                        yellow2 += 1
                total2 = green2 + yellow2 + red2
                green_p2 = round(green2 / total2 * 100, 2)
                yellow_p2 = round(yellow2 / total2 * 100, 2)
                red_p2 = round(red2 / total2 * 100, 2)
                data_set = green_p2, yellow_p2, red_p2
                percentage_of_paring.append(data_set)
                lista = list(percentage_of_paring)
            lista.append(A, )
            total_percentage.append(lista)
        ctx = {
            "tournament": tournament,
            "paring": player,
            "form": form,
            "green": green,
            "yellow": yellow,
            "red": red,
            "green_p": green_p,
            "yellow_p": yellow_p,
            "red_p": red_p,
            "players_points": players_points,
            "army_points": army_points,
            "total_percentage": total_percentage,
            "teamB": teamB,
        }
        return render(request, "paring_8v8.html", ctx)

    def post(self, request, id, par):
        tournament = TournamentETC.objects.get(pk=id)
        player = Team_of_8.objects.get(pk=par)
        form = FirstParingsForm(request.POST)
        if form.is_valid():
            first_p1 = form.cleaned_data["first_p1"].short_name
            first_op1 = form.cleaned_data["first_op1"].short_name
            first_p2 = form.cleaned_data["first_p2"].short_name
            first_op2 = form.cleaned_data["first_op2"].short_name
            result = []
            data_list = []
            rating = []
            players_points = []
            army_points = []
            for w in range(1, 9):
                p1points = []
                attr2 = f'player_name_{w}'
                attr3 = f'p{w}'
                for z in range(1, 9):
                    attr1 = f'p{w}{z}'
                    j1 = getattr(player, attr1)
                    p1points.append(j1)
                av1 = round(sum(p1points) / 8, 2)
                p1points.append(av1)
                player_name = getattr(tournament, attr2)
                player_army = getattr(tournament, attr3)
                player_data = player_name, player_army
                player_p = p1points, player_data
                players_points.append(player_p)
            for w in range(1, 9):
                p2points = []
                for z in range(1, 9):
                    attr2 = f'p{z}{w}'
                    j2 = getattr(player, attr2)
                    p2points.append(j2)
                av2 = round(sum(p2points) / 8, 2)
                army_points.append(av2)
            teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4,
                     tournament.p5, tournament.p6, tournament.p7, tournament.p8]
            # teamA.remove(first_p1)
            # teamA.remove(first_p2)
            teamB = [player.op1, player.op2, player.op3, player.op4,
                     player.op5, player.op6, player.op7, player.op8]
            # teamB.remove(first_op1)
            # teamB.remove(first_op2)
            for perm in permutations(teamA):
                result.append(list(zip(perm, teamB)))
            for pairing in result:
                total = 0
                for i in pairing:
                    points = []
                    for A in teamA:
                        for B in teamB:
                            if i == (A, B):
                                x = teamA.index(A) + 1
                                y = teamB.index(B) + 1
                                attr = f"p{x}{y}"
                                j = getattr(player, attr)
                                # i = player.p11 ...
                            points.append(j)
                    total += j
                    average = total / 8
                data_list.append([pairing, total, average])
            sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
            filtered_list = []
            pre_list = []
            for i in range(len(data_list) - 1):
                for j in range(8):
                    if data_list[i][0][j] == (first_p1, first_op1):
                        pre_list.append(data_list[i])
            for i in range(len(pre_list) - 1):
                for j in range(8):
                    if pre_list[i][0][j] == (first_p2, first_op2):
                        filtered_list.append(pre_list[i])
            sorted_filtered_list = sorted(filtered_list, key=itemgetter(2), reverse=True)
            green = 0
            yellow = 0
            red = 0
            for i in sorted_filtered_list:
                if i[2] > 0:
                    green += 1
                elif i[2] < 0:
                    red += 1
                else:
                    yellow += 1
            total = green+yellow+red
            green_p = green / total * 100
            yellow_p = yellow / total * 100
            red_p = red / total * 100
            # next_paring = sorted(players_points, key=lambda x: x[0][8], reverse=True)
            # rating = next_paring[0][1][1]
            # for i in range(len(sorted_filtered_list)-1):
            #     for j in range(8):
            #         if sorted_filtered_list[i][1][j] > 12:
            #             next_paring.append(sorted_filtered_list[i][0][j][0])
            # rating = dict((i, next_paring.count(i)) for i in next_paring)
            # if first_p1 in rating:
            #     del rating[first_p1]
            # if first_p2 in rating:
            #     del rating[first_p2]
            ctx = {
                "tournament": tournament,
                "paring": player,
                "first_p1": first_p1,
                "first_p2": first_p2,
                "first_op1": first_op1,
                "first_op2": first_op2,
                "green": green,
                "yellow": yellow,
                "red": red,
                "green_p": green_p,
                "yellow_p": yellow_p,
                "red_p": red_p,
                "best_armies": rating[:3],
                "army_points": army_points,
                "players_points": players_points,
                "teamB": teamB,
            }
            return render(request, "paring_8v8.html", ctx)


class EditTParing8v8View(View):
    def get(self, request, id, par):
        tournament = TournamentETC.objects.get(pk=id)
        parings_list = Team_of_8.objects.filter(tournament=tournament.id).order_by("name")
        paring = Team_of_8.objects.get(pk=par)
        form = TParings8Form(instance=paring)
        ctx = {
            "tournament": tournament,
            "form": form,
            "parings_list": parings_list,
        }
        return render(request, "etc_parings.html", ctx)

    def post(self, request, id, par):
        tournament = TournamentETC.objects.get(pk=id)
        paring = Team_of_8.objects.get(pk=par)
        form = TParings8Form(request.POST, instance=paring)
        if form.is_valid():
            result = form.save(commit=False)
            result.tournament = tournament
            result.save()
            return redirect("paring-etc-view", id=id, par=par)


class DeleteTParing8v8View(View):
    def get(self, request, id, par):
        p = Team_of_8.objects.get(pk=par)
        p.delete()
        return redirect("etc-parings", id=id)



# poprzednia wersja 8v8

# class TParing8v8View(View):
#     def get(self, request, id, par):
#         tournament = TournamentETC.objects.get(pk=id)
#         player = Team_of_8.objects.get(pk=par)
#         form = FirstParingsForm()
#         result = []
#         data_list = []
#         mp = []
#         player_points = []
#         army_points = []
#         for w in range(1, 9):
#             p1points = []
#             for z in range(1, 9):
#                 attr1 = f'p{w}{z}'
#                 j1 = getattr(player, attr1)
#                 p1points.append(j1)
#             av1 = round(sum(p1points) / 8, 2)
#             p1points.append(av1)
#             player_points.append(p1points)
#         for w in range(1, 9):
#             p2points = []
#             for z in range(1, 9):
#                 attr2 = f'p{z}{w}'
#                 j2 = getattr(player, attr2)
#                 p2points.append(j2)
#             av2 = round(sum(p2points) / 8, 2)
#             army_points.append(av2)
#         teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4,
#                  tournament.p5, tournament.p6, tournament.p7, tournament.p8]
#         teamB = [player.op1, player.op2, player.op3, player.op4,
#                  player.op5, player.op6, player.op7, player.op8]
#         for perm in permutations(teamA):
#             result.append(list(zip(perm, teamB)))
#         for pairing in result:
#             score = []
#             total = 0
#             for i in pairing:
#                 points = []
#                 for A in teamA:
#                     for B in teamB:
#                         if i == (A, B):
#                             x = teamA.index(A) + 1
#                             y = teamB.index(B) + 1
#                             attr = f"p{x}{y}"
#                             j = getattr(player, attr)
#                             # i = player.p11 ...
#                         points.append(j)
#                 for s in points:
#                     if s == -3:
#                         mp = 1
#                     elif s == -2:
#                         mp = 4
#                     elif s == -1:
#                         mp = 7
#                     elif s == 1:
#                         mp = 13
#                     elif s == 2:
#                         mp = 16
#                     elif s == 3:
#                         mp = 19
#                     else:
#                         mp = 10
#                 score.append(mp)
#                 total += mp
#             data_list.append([pairing, score, total])
#         sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
#         green = 0
#         yellow = 0
#         red = 0
#         for i in sorted_list:
#             if i[2] > 81:
#                 green += 1
#             elif i[2] < 79:
#                 red += 1
#             else:
#                 yellow += 1
#         total = green + yellow + red
#         green_p = green / total * 100
#         yellow_p = yellow / total * 100
#         red_p = red / total * 100
#         ctx = {
#             "tournament": tournament,
#             "paring": player,
#             "form": form,
#             # "data_list": sorted_list[:6],
#             # "data_list_bad": sorted_list[-6:],
#             "green": green,
#             "yellow": yellow,
#             "red": red,
#             "green_p": green_p,
#             "yellow_p": yellow_p,
#             "red_p": red_p,
#             "p1points": player_points[0],
#             "p2points": player_points[1],
#             "p3points": player_points[2],
#             "p4points": player_points[3],
#             "p5points": player_points[4],
#             "p6points": player_points[5],
#             "p7points": player_points[6],
#             "p8points": player_points[7],
#             "army_points": army_points,
#         }
#         return render(request, "paring_8v8.html", ctx)
#
#     def post(self, request, id, par):
#         tournament = TournamentETC.objects.get(pk=id)
#         player = Team_of_8.objects.get(pk=par)
#         form = FirstParingsForm(request.POST)
#         if form.is_valid():
#             first_p1 = form.cleaned_data["first_p1"].short_name
#             first_op1 = form.cleaned_data["first_op1"].short_name
#             first_p2 = form.cleaned_data["first_p2"].short_name
#             first_op2 = form.cleaned_data["first_op2"].short_name
#             result = []
#             data_list = []
#             mp = []
#             player_points = []
#             army_points = []
#             for w in range(1, 9):
#                 p1points = []
#                 for z in range(1, 9):
#                     attr1 = f'p{w}{z}'
#                     j1 = getattr(player, attr1)
#                     p1points.append(j1)
#                 av1 = round(sum(p1points) / 8, 2)
#                 p1points.append(av1)
#                 player_points.append(p1points)
#             for w in range(1, 9):
#                 p2points = []
#                 for z in range(1, 9):
#                     attr2 = f'p{z}{w}'
#                     j2 = getattr(player, attr2)
#                     p2points.append(j2)
#                 av2 = round(sum(p2points) / 8, 2)
#                 army_points.append(av2)
#             teamA = [tournament.p1, tournament.p2, tournament.p3, tournament.p4,
#                      tournament.p5, tournament.p6, tournament.p7, tournament.p8]
#             # teamA.remove(first_p1)
#             # teamA.remove(first_p2)
#             teamB = [player.op1, player.op2, player.op3, player.op4,
#                      player.op5, player.op6, player.op7, player.op8]
#             # teamB.remove(first_op1)
#             # teamB.remove(first_op2)
#             for perm in permutations(teamA):
#                 result.append(list(zip(perm, teamB)))
#             for pairing in result:
#                 score = []
#                 total = 0
#                 for i in pairing:
#                     points = []
#                     for A in teamA:
#                         for B in teamB:
#                             if i == (A, B):
#                                 x = teamA.index(A) + 1
#                                 y = teamB.index(B) + 1
#                                 attr = f"p{x}{y}"
#                                 j = getattr(player, attr)
#                                 # i = player.p11 ...
#                             points.append(j)
#                     for s in points:
#                         if s == -3:
#                             mp = 1
#                         elif s == -2:
#                             mp = 4
#                         elif s == -1:
#                             mp = 7
#                         elif s == 1:
#                             mp = 13
#                         elif s == 2:
#                             mp = 16
#                         elif s == 3:
#                             mp = 19
#                         else:
#                             mp = 10
#                     score.append(mp)
#                     total += mp
#                 data_list.append([pairing, score, total])
#             sorted_list = sorted(data_list, key=itemgetter(2), reverse=True)
#             filtered_list = []
#             pre_list = []
#             for i in range(len(data_list) - 1):
#                 for j in range(8):
#                     if data_list[i][0][j] == (first_p1, first_op1):
#                         pre_list.append(data_list[i])
#             for i in range(len(pre_list) - 1):
#                 for j in range(8):
#                     if pre_list[i][0][j] == (first_p2, first_op2):
#                         filtered_list.append(pre_list[i])
#             sorted_filtered_list = sorted(filtered_list, key=itemgetter(2), reverse=True)
#             next_paring = []
#             for i in range(len(sorted_filtered_list)-1):
#                 for j in range(8):
#                     if sorted_filtered_list[i][1][j] > 12:
#                         next_paring.append(sorted_filtered_list[i][0][j][0])
#             rating = dict((i, next_paring.count(i)) for i in next_paring)
#             if first_p1 in rating:
#                 del rating[first_p1]
#             if first_p2 in rating:
#                 del rating[first_p2]
#             green = 0
#             yellow = 0
#             red = 0
#             for i in sorted_filtered_list:
#                 if i[2] > 81:
#                     green += 1
#                 elif i[2] < 79:
#                     red += 1
#                 else:
#                     yellow += 1
#             total = green+yellow+red
#             green_p = green / total * 100
#             yellow_p = yellow / total * 100
#             red_p = red / total * 100
#             ctx = {
#                 "tournament": tournament,
#                 "paring": player,
#                 # "data_list": sorted_list[:6],
#                 # "data_list_bad": sorted_list[-6:],
#                 # "filtered_list": sorted_filtered_list,
#                 "first_p1": first_p1,
#                 "first_p2": first_p2,
#                 "first_op1": first_op1,
#                 "first_op2": first_op2,
#                 "green": green,
#                 "yellow": yellow,
#                 "red": red,
#                 "green_p": green_p,
#                 "yellow_p": yellow_p,
#                 "red_p": red_p,
#                 "best_armies": rating,
#                 "p1points": player_points[0],
#                 "p2points": player_points[1],
#                 "p3points": player_points[2],
#                 "p4points": player_points[3],
#                 "p5points": player_points[4],
#                 "p6points": player_points[5],
#                 "p7points": player_points[6],
#                 "p8points": player_points[7],
#                 "army_points": army_points,
#             }
#             return render(request, "paring_8v8.html", ctx)
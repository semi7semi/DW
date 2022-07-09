from django.contrib import admin
from django.urls import path

from wfb_app.views import Index, List, AddUnitView, EditUnitView, RankingList, \
    LoginView, LogoutView, UsersList, CreateUserView, EditUserView, AddGameResultView, DeleteUser, UserDetailsView, \
    ArmyListView, ArmyDetailsView, DeleteUnitView, EditGameResultView, CalcView, Landing_page, RollDiceView, TableView, \
    RankingList_2020, UserDetailsView_2020, Index_2020, Index_2021, UserDetailsView_2021, RankingList_2021, \
    TournamentsView, AddTournamentView, DeleteTournamentView, EditTournamentView, TournamentParingsView, TParing3v3View, \
    DeleteTParing3v3View, EditTParing3v3View, TParing4v4View, DeleteTParing4v4View, TParing5v5View, \
    DeleteTParing5v5View, EditTParing4v4View, EditTParing5v5View, ArmyIconsView, TournamentETCView, \
    AddTournamentETCView, EditTournamentETCView, DeleteTournamentETCView, ETCParingsView, TParing8v8View, \
    DeleteTParing8v8View

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', Index.as_view(), name="main"),
    path('', Landing_page.as_view(), name="dashboard"),


    path("add_unit/", AddUnitView.as_view(), name="add-unit"),
    path('units_list/', List.as_view(), name="units-list"),
    path('edit_unit/<int:id>/', EditUnitView.as_view(), name="edit-unit"),
    path("delete_unit/<int:id>/", DeleteUnitView.as_view()),
    path("army_list/", ArmyListView.as_view(), name="army-list"),
    path("army_details/<int:id>/", ArmyDetailsView.as_view(), name="army-details"),
    path("calculator/", CalcView.as_view(), name="calc-view"),

    path("ranking/", RankingList.as_view(), name="ranking-list"),
    path("ranking/add_result/", AddGameResultView.as_view(), name="result"),
    path("ranking/edit/<int:id>/", EditGameResultView.as_view(), name="result-edit"),

    path("accounts/login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("users/", UsersList.as_view(), name="users-list"),
    path("add_user/", CreateUserView.as_view(), name="register"),
    path("edit_user/<int:id>/", EditUserView.as_view(), name="edit-user"),
    path("user_details/<int:id>/", UserDetailsView.as_view(), name="user-details"),
    path("edit_user/delete/<int:id>/", DeleteUser.as_view(), name="delete-user"),
    path("dice/", RollDiceView.as_view(), name="dice-view"),
    path("tables/", TableView.as_view(), name="table-view"),

    path("user_details_2020/<int:id>/", UserDetailsView_2020.as_view(), name="user-details-2020"),
    path("ranking_2020/", RankingList_2020.as_view(), name="ranking-list-2020"),
    path('index_2020/', Index_2020.as_view(), name="main-2020"),

    path("user_details_2021/<int:id>/", UserDetailsView_2021.as_view(), name="user-details-2021"),
    path("ranking_2021/", RankingList_2021.as_view(), name="ranking-list-2021"),
    path('index_2021/', Index_2021.as_view(), name="main-2021"),

    path("tournaments/", TournamentsView.as_view(), name="tournaments-view"),
    path("tournaments/add/", AddTournamentView.as_view(), name="add-tournament"),
    path("tournaments/delete/<int:id>/", DeleteTournamentView.as_view(), name="delete-tournament"),
    path("tournaments/edit/<int:id>/", EditTournamentView.as_view(), name="edit-tournament"),
    path("tournaments/<int:id>/", TournamentParingsView.as_view(), name="tournament-parings"),

    path("t3v3/<int:id>/<int:par>/", TParing3v3View.as_view(), name="paring-3v3-view"),
    path("t3v3/<int:id>/<int:par>/delete/", DeleteTParing3v3View.as_view(), name="delete-paring-3v3"),
    path("t3v3/<int:id>/<int:par>/edit/", EditTParing3v3View.as_view(), name="edit-paring-3v3"),

    path("t4v4/<int:id>/<int:par>/", TParing4v4View.as_view(), name="paring-4v4-view"),
    path("t4v4/<int:id>/<int:par>/delete/", DeleteTParing4v4View.as_view(), name="delete-paring-4v4"),
    path("t4v4/<int:id>/<int:par>/edit/", EditTParing4v4View.as_view(), name="edit-paring-4v4"),

    path("t5v5/<int:id>/<int:par>/", TParing5v5View.as_view(), name="paring-5v5-view"),
    path("t5v5/<int:id>/<int:par>/delete/", DeleteTParing5v5View.as_view(), name="delete-paring-5v5"),
    path("t5v5/<int:id>/<int:par>/edit/", EditTParing5v5View.as_view(), name="edit-paring-5v5"),

    path("tournaments/army_icons/", ArmyIconsView.as_view(), name="army-icons"),

    path("etc/", TournamentETCView.as_view(), name="etc-view"),
    path("etc/add/", AddTournamentETCView.as_view(), name="add-etc"),
    path("etc/delete/<int:id>/", DeleteTournamentETCView.as_view(), name="delete-etc"),
    path("etc/edit/<int:id>/", EditTournamentETCView.as_view(), name="edit-etc"),
    path("etc/<int:id>/", ETCParingsView.as_view(), name="etc-parings"),
    path("etc/<int:id>/<int:par>/", TParing8v8View.as_view(), name="paring-etc-view"),
    path("etc/<int:id>/<int:par>/delete/", DeleteTParing8v8View.as_view(), name="delete-paring-etc")


]


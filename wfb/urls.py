from django.contrib import admin
from django.urls import path

from wfb_app.views import Index, List, AddUnitView, EditUnitView, RankingList, \
    LoginView, LogoutView, UsersList, CreateUserView, EditUserView, AddGameResultView, DeleteUser, UserDetailsView, \
    ArmyListView, ArmyDetailsView, DeleteUnitView, EditGameResultView, CalcView, Landing_page, RollDiceView, TableView, \
    RankingList_2020, UserDetailsView_2020, Index_2020, ParingsView, DeleteParingView, AddParingView, ParingDetailsView

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

    path("parings/", ParingsView.as_view(), name="parings-view"),
    path("add_paring/", AddParingView.as_view(), name="add-paring"),
    path("delete_paring/<int:id>/", DeleteParingView.as_view(), name="delete-paring"),
    path("paring/<int:id>/", ParingDetailsView.as_view(), name="paring-details"),

    path("user_details_2020/<int:id>/", UserDetailsView_2020.as_view(), name="user-details-2020"),
    path("ranking_2020/", RankingList_2020.as_view(), name="ranking-list-2020"),
    path('index_2020/', Index_2020.as_view(), name="main-2020"),
]

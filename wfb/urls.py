from django.contrib import admin
from django.urls import path

from wfb_app.views import Index, List, Calc, AddUnitView, EditUnitView, RankingList, \
    LoginView, LogoutView, UsersList, CreateUserView, EditUserView, AddGameResultView, DeleteUser, UserDetailsView, \
    ArmyListView, ArmyDetailsView, DeleteUnitView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name="main"),


    path("add_unit/", AddUnitView.as_view(), name="add-unit"),
    path('units_list/', List.as_view(), name="units-list"),
    path('edit_unit/<int:id>/', EditUnitView.as_view(), name="edit-unit"),
    path("delete_unit/<int:id>/", DeleteUnitView.as_view()),
    path("army_list/", ArmyListView.as_view()),
    path("army_details/<int:id>/", ArmyDetailsView.as_view()),
    path('calculator/', Calc.as_view(), name="calc-view"),

    path("ranking/", RankingList.as_view(), name="ranking-list"),
    path("ranking/add_result/", AddGameResultView.as_view()),

    path("accounts/login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout-user"),
    path("users/", UsersList.as_view(), name="users-list"),
    path("add_user/", CreateUserView.as_view()),
    path("edit_user/<int:id>/", EditUserView.as_view()),
    path("user_details/<int:id>/", UserDetailsView.as_view(), name="user-details"),
    path("users/delete/<int:id>/", DeleteUser.as_view()),
]

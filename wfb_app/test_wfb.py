import pytest
from django.contrib.auth.models import User
from wfb_app.models import Units, Armys, Objectives, GameResults
from datetime import datetime

@pytest.mark.django_db
def test_users_list(client, user):
    response = client.post("/users/")
    assert response.status_code == 302
    assert User.objects.count() == 1
    u = User.objects.get(username=user.username)
    assert u.username == user.username


@pytest.mark.django_db
def test_users_details(client, user):
    response = client.post(f"/user_details/{user.pk}")
    assert response.status_code == 301


@pytest.mark.django_db
def test_add_user(client, army):
    # sprawdzamy czy baza jest pusta
    assert len(User.objects.all()) == 0
    assert len(Armys.objects.all()) == 1
    # tworzymy obiekty
    response = client.post("/add_user/", {
        "username": "Marcin",
        "password": "1234",
        "password_2": "1234",
        "email": "aa@aa.pl",
        "user_army": army.short_name
    })
    assert len(User.objects.all()) == 1
    assert response.status_code == 302
    user = User.objects.get(username="Marcin")
    assert user.username == "Marcin"
    assert user.email == "aa@aa.pl"
    assert user.profile.user_army == "WDG"


@pytest.mark.django_db
def test_add_unit(client, user):
    # sprawdzamy czy baza jest pusta
    assert len(Units.objects.all()) == 0
    # logujemy uzytkownika bo widok jest zabezpieczony
    client.force_login(user)
    # tworzymy obiekty
    response = client.post("/add_unit/", {
        "name": "Barbarian",
        "offensive": 4,
        "strength": 3,
        "ap": 0,
    })
    assert response.status_code == 302
    assert len(Units.objects.all()) == 1
    unit = Units.objects.get(name="Barbarian")
    assert unit.name == "Barbarian"
    assert unit.offensive == 4
    assert unit.strength == 3
    assert unit.ap == 0
    assert unit.reflex == False
    assert unit.army.name == "Beast Herds"


@pytest.mark.django_db
def test_add_result(client, user):
    assert len(GameResults.objects.all()) == 0
    # logujemy uzytkownika bo widok jest zabezpieczony
    client.force_login(user)
    # tworzymy obiekty
    response = client.post("/ranking/add_result/", {
        "user": user.id,
        "battle_points": 10,
        "objective": True,
        "objective_type": "1",
        "game_rank": "master",
        "opponent": "Przeciwnik",
    })
    assert response.status_code == 302
    assert len(GameResults.objects.all()) == 1
    result = GameResults.objects.get(user=user.id)
    assert result.battle_points == 10
    assert result.game_rank == "master"
    assert result.objective_type == "1"
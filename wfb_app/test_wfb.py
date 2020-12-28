import pytest
from django.contrib.auth.models import User
from wfb_app.models import Units, Armys, GameResults

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
def test_ranking_list(client):
    response = client.get(f"/ranking/")
    assert response.status_code == 200


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
def test_add_unit(client, user, army):
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
        "reflex": False,
        "army": army.id
    })
    assert response.status_code == 302
    assert len(Units.objects.all()) == 1
    unit = Units.objects.get(name="Barbarian")
    assert unit.name == "Barbarian"
    assert unit.offensive == 4
    assert unit.strength == 3
    assert unit.ap == 0
    assert unit.reflex == False
    assert unit.army.name == "Warriors of the Dark Gods"


@pytest.mark.django_db
def test_edit_unit(client, user, unit, army):
    # sprawdzamy czy jest cos w wbazie
    assert len(Units.objects.all()) == 1
    unit = Units.objects.get(name="Barbarian")
    assert unit.name == "Barbarian"
    assert unit.offensive == 3
    assert unit.strength == 3
    assert unit.ap == 1
    assert unit.reflex == False
    assert unit.army.name == "Warriors of the Dark Gods"
    # logujemy uzytkownika bo widok jest zabezpieczony
    client.force_login(user)
    # edytujemy obiekty
    response = client.post(f"/edit_unit/{unit.id}/", {
        "name": "Warrior",
        "offensive": 4,
        "strength": 4,
        "ap": 10,
        "reflex": False,
        "army": army.id
    })
    assert response.status_code == 302
    assert len(Units.objects.all()) == 1
    unit = Units.objects.get(name="Warrior")
    assert unit.name == "Warrior"
    assert unit.offensive == 4
    assert unit.strength == 4
    assert unit.ap == 10
    assert unit.reflex == False
    assert unit.army.name == "Warriors of the Dark Gods"


@pytest.mark.django_db
def test_add_result(client, user):
    assert len(GameResults.objects.all()) == 0
    # logujemy uzytkownika bo widok jest zabezpieczony
    client.force_login(user)
    # tworzymy obiekty
    response = client.post("/ranking/add_result/", {
        "battle_points": 10,
        "objective_type": "1",
        "game_rank": "local",
        "opponent": "Stefan",
        "date":"2020-12-12"
    })
    assert response.status_code == 302
    assert len(GameResults.objects.all()) == 1
    result = GameResults.objects.get(user=user.id)
    assert result.battle_points == 10
    assert result.game_rank == "local"
    assert result.objective_type == "1"
    assert result.opponent == "Stefan"
    assert str(result.date) == "2020-12-12"


@pytest.mark.django_db
def test_edit_result(client, user):
    GameResults.objects.create(
        user=user,
        battle_points=20,
        objective=True,
        objective_type="1",
        game_rank="home",
        opponent="Semi",
        date="2021-01-01"
    )
    assert len(GameResults.objects.all()) == 1
    result = GameResults.objects.first()
    assert result.battle_points == 20
    assert result.game_rank == "home"
    assert result.objective_type == "1"
    assert result.opponent == "Semi"
    assert str(result.date) == "2021-01-01"
    # logujemy uzytkownika bo widok jest zabezpieczony
    client.force_login(user)
    # Edytujemy obiekt
    response = client.post(f"/ranking/edit/{result.id}/", {
        "battle_points": 10,
        "objective_type": "1",
        "game_rank": "local",
        "opponent": "Stefan",
        "date":"2021-01-10"
    })
    assert response.status_code == 302
    assert len(GameResults.objects.all()) == 1
    result = GameResults.objects.get(user=user)
    assert result.battle_points == 10
    assert result.game_rank == "local"
    assert result.objective_type == "1"
    assert result.opponent == "Stefan"
    assert str(result.date) == "2021-01-10"


@pytest.mark.django_db
def test_calculator(client, user, unit):
    # Sprawdzamy czy cos jest w bazie
    assert len(Units.objects.all()) == 1
    # logujemy klienta
    client.force_login(user)
    # podajemy dane wejsciowe
    response = client.post("/calculator/", {
        "unit_name": f"{unit.id}",
        "attacks": 10,
        "defensive": 3,
        "resistance": 3,
    })
    assert response.status_code == 200
    assert response.context["hit"] == 5
    assert response.context["wounds"] == 2.5
    assert response.context["unit"] == unit


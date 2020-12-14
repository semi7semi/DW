from django.contrib.auth.models import User
from django.test import Client
import pytest
from wfb_app.models import Units, Armys


@pytest.fixture
def client():
    c = Client()
    return c


@pytest.fixture
def user():
    user = User.objects.create(
        username="semi",
        password="1234",
        email="aaa@aa.pl",
    )
    return user


@pytest.fixture
def army():
    army = Armys.objects.create(name="Warriors of the Dark Gods", short_name="WDG", description="Opis WDG")
    return army


@pytest.fixture
def unit():
    army = Armys.objects.create(name="Warriors of the Dark Gods", short_name="WDG", description="Opis armii WDG")
    one_unit = Units.objects.create(name="Barbarian", offensive=3, strength=3, ap=1, reflex=False, army=army.id)
    return one_unit

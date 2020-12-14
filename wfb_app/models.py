from django.db import models
from django.contrib.auth.models import User


ARMIES_CHOICE = (
    ("BH", "Beast Herds"),
    ("DL", "Demonic Legion"),
    ("DE", "Dread Elves"),
    ("DH", "Dvarwen Holds"),
    ("EoS", "Empire of Sonnstahl"),
    ("HE", "Highborn Elves"),
    ("ID", "Infernal Dwarves"),
    ("KoE", "Kingdome of Equitaine"),
    ("OK", "Ogre Khans"),
    ("OG", "Orcs and Goblins"),
    ("SA", "Saurian Ancients"),
    ("SE", "Sylvan Elves"),
    ("UD", "Undying Dynasties"),
    ("VC", "Vampire Covenant"),
    ("VS", "Vermin Swarm"),
    ("WDG", "Warriors of the Dark Gods")
)

GAME_RANK = (
    ("master", "Master"),
    ("local", "Local"),
    ("home", "Home")
)

OBJ = (
    ("1", "Hold the Ground"),
    ("2", "Breakthrough"),
    ("3", "Spoils of War"),
    ("4", "King of the Hill"),
    ("5", "Capture the Flag"),
    ("6", "Secure Target")
)


class Armys(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Units(models.Model):
    name = models.CharField(max_length=64, unique=True)
    offensive = models.IntegerField()
    strength = models.IntegerField()
    ap = models.IntegerField()
    reflex = models.BooleanField(default=False)
    army = models.ForeignKey(Armys, on_delete=models.CASCADE, default=1)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_army = models.CharField(max_length=32, choices=ARMIES_CHOICE)


class GameResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    battle_points = models.IntegerField()
    objective = models.BooleanField(default=False)
    objective_type = models.CharField(max_length=32, choices=OBJ, blank=True)
    game_rank = models.CharField(max_length=16, choices=GAME_RANK)
    opponent = models.CharField(max_length=64)
    date = models.DateField(auto_now_add=True)



class Objectives(models.Model):
    name = models.CharField(max_length=32, choices=OBJ)

    def __str__(self):
        return self.name

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

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_army = models.CharField(max_length=32, choices=ARMIES_CHOICE)


class GameResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    army = models.CharField(max_length=32, choices=ARMIES_CHOICE, null=True, blank=True, default=None)
    battle_points = models.IntegerField()
    objective = models.BooleanField(default=False)
    objective_type = models.CharField(max_length=32, choices=OBJ, blank=True)
    game_rank = models.CharField(max_length=16, choices=GAME_RANK)
    opponent_dw = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name= 'from_dw')
    opponent = models.CharField(max_length=64, blank=True, null=True)
    opponent_army = models.CharField(max_length=32, choices=ARMIES_CHOICE, null=True, blank=True, default=None)
    date = models.DateField()

    date.editable = True

class Objectives(models.Model):
    name = models.CharField(max_length=32, choices=OBJ)

    def __str__(self):
        return self.name


class Parings_3(models.Model):
    name = models.CharField(max_length=64)
    p1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField()
    p12 = models.IntegerField()
    p13 = models.IntegerField()
    p21 = models.IntegerField()
    p22 = models.IntegerField()
    p23 = models.IntegerField()
    p31 = models.IntegerField()
    p32 = models.IntegerField()
    p33 = models.IntegerField()
    date = models.DateField(auto_now_add=True)


class Parings_4(models.Model):
    name = models.CharField(max_length=64)
    p1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField()
    p12 = models.IntegerField()
    p13 = models.IntegerField()
    p14 = models.IntegerField()
    p21 = models.IntegerField()
    p22 = models.IntegerField()
    p23 = models.IntegerField()
    p24 = models.IntegerField()
    p31 = models.IntegerField()
    p32 = models.IntegerField()
    p33 = models.IntegerField()
    p34 = models.IntegerField()
    p41 = models.IntegerField()
    p42 = models.IntegerField()
    p43 = models.IntegerField()
    p44 = models.IntegerField()
    date = models.DateField(auto_now_add=True)



class Parings_5(models.Model):
    name = models.CharField(max_length=64)
    p1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p5 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op5 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField()
    p12 = models.IntegerField()
    p13 = models.IntegerField()
    p14 = models.IntegerField()
    p15 = models.IntegerField()
    p21 = models.IntegerField()
    p22 = models.IntegerField()
    p23 = models.IntegerField()
    p24 = models.IntegerField()
    p25 = models.IntegerField()
    p31 = models.IntegerField()
    p32 = models.IntegerField()
    p33 = models.IntegerField()
    p34 = models.IntegerField()
    p35 = models.IntegerField()
    p41 = models.IntegerField()
    p42 = models.IntegerField()
    p43 = models.IntegerField()
    p44 = models.IntegerField()
    p45 = models.IntegerField()
    p51 = models.IntegerField()
    p52 = models.IntegerField()
    p53 = models.IntegerField()
    p54 = models.IntegerField()
    p55 = models.IntegerField()
    date = models.DateField(auto_now_add=True)

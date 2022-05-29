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

PARING_SCORE_CHOICES = ((-2, "-2"), (-1, "-1"), (0, "0"), (1, "1"), (2, "2"))



class Armys(models.Model):
    name = models.CharField(max_length=32)
    short_name = models.CharField(max_length=16)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True)

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
    opponent_dw = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None,
                                    related_name='from_dw')
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


class Tournaments(models.Model):
    name = models.CharField(max_length=64)
    no_of_players = models.IntegerField()
    player_name_1 = models.CharField(max_length=64)
    player_name_2 = models.CharField(max_length=64)
    player_name_3 = models.CharField(max_length=64)
    player_name_4 = models.CharField(max_length=64, null=True, blank=True, default=None)
    player_name_5 = models.CharField(max_length=64, null=True, blank=True, default=None)
    p1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p4 = models.CharField(max_length=16, choices=ARMIES_CHOICE, null=True, blank=True, default=None)
    p5 = models.CharField(max_length=16, choices=ARMIES_CHOICE, null=True, blank=True, default=None)
    date = models.DateField()

    date.editable = True


class Team_of_3(models.Model):
    name = models.CharField(max_length=16)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p12 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p13 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p21 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p22 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p23 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p31 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p32 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p33 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, related_name='tourney3')

class Team_of_4(models.Model):
    name = models.CharField(max_length=64)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p12 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p13 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p14 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p21 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p22 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p23 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p24 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p31 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p32 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p33 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p34 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p41 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p42 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p43 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p44 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, related_name='tourney4')

class Team_of_5(models.Model):
    name = models.CharField(max_length=64)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    op5 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p11 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p12 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p13 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p14 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p15 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p21 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p22 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p23 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p24 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p25 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p31 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p32 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p33 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p34 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p35 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p41 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p42 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p43 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p44 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p45 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p51 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p52 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p53 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p54 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p55 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    tournament = models.ForeignKey(Tournaments, on_delete=models.CASCADE, related_name='tourney5')
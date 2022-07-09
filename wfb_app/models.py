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

ARMIES_CHOICE2 = (
    ("BH", "BH"),
    ("DL", "DL"),
    ("DE", "DE"),
    ("DH", "DH"),
    ("EoS", "EoS"),
    ("HE", "HE"),
    ("ID", "ID"),
    ("KoE", "KoE"),
    ("OK", "OK"),
    ("OG", "OG"),
    ("SA", "SA"),
    ("SE", "SE"),
    ("UD", "UD"),
    ("VC", "VC"),
    ("VS", "VS"),
    ("WDG", "WDG")
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

PARING_SCORE_CHOICES = ((-3, "-3"), (-2, "-2"), (-1, "-1"), (0, "0"), (1, "1"), (2, "2"), (3, "3"))



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
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op5 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
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


class TournamentETC(models.Model):
    name = models.CharField(max_length=64)
    player_name_1 = models.CharField(max_length=64)
    player_name_2 = models.CharField(max_length=64)
    player_name_3 = models.CharField(max_length=64)
    player_name_4 = models.CharField(max_length=64)
    player_name_5 = models.CharField(max_length=64)
    player_name_6 = models.CharField(max_length=64)
    player_name_7 = models.CharField(max_length=64)
    player_name_8 = models.CharField(max_length=64)
    p1 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p2 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p3 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p4 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p5 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p6 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p7 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    p8 = models.CharField(max_length=16, choices=ARMIES_CHOICE)
    date = models.DateField()

    date.editable = True


class Team_of_8(models.Model):
    name = models.CharField(max_length=64)
    op1 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op2 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op3 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op4 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op5 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op6 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op7 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    op8 = models.CharField(max_length=16, choices=ARMIES_CHOICE2)
    p11 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p12 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p13 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p14 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p15 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p16 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p17 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p18 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p21 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p22 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p23 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p24 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p25 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p26 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p27 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p28 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p31 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p32 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p33 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p34 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p35 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p36 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p37 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p38 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p41 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p42 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p43 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p44 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p45 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p46 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p47 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p48 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p51 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p52 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p53 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p54 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p55 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p56 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p57 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p58 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p61 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p62 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p63 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p64 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p65 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p66 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p67 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p68 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p71 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p72 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p73 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p74 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p75 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p76 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p77 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p78 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p81 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p82 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p83 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p84 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p85 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p86 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p87 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    p88 = models.IntegerField(choices=PARING_SCORE_CHOICES)
    tournament = models.ForeignKey(TournamentETC, on_delete=models.CASCADE, related_name='tourney8')

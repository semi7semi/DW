
def towound(hit, st, res):
    if st - res >= 2:
        wounds = hit * 5 / 6
    elif 2 > st - res >= 1:
        wounds = hit * 2 / 3
    elif 1 > st - res >= 0:
        wounds = hit / 2
    elif 0 > st - res >= -1:
        wounds = hit / 3
    else:
        wounds = hit / 6
    return round(wounds, 1)


def afterarmour(ap, arm, wounds):
    if arm - ap <= 0:
        wounds_armour = wounds
    elif 0 < arm - ap <= 1:
        wounds_armour = wounds * 5 / 6
    elif 1 < arm - ap <= 2:
        wounds_armour = wounds * 2 / 3
    elif 2 < arm - ap <= 3:
        wounds_armour = wounds / 2
    elif 3 < arm - ap <= 4:
        wounds_armour = wounds / 3
    else:
        wounds_armour = wounds / 6
    return round(wounds_armour, 1)


def takeSecond(elem):
    return elem[1]

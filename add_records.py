from wfb_app.models import Armys


ARMIES_CHOICE = (
    ("BH", "Beast Herds", "Bestie"),
    ("DL", "Demonic Legion", "Demony"),
    ("DE", "Dread Elves", "Mroczne Elfy"),
    ("DH", "Dvarwen Holds", "Krasnoludy"),
    ("EoS", "Empire of Sonnstahl", "Imperium"),
    ("HE", "Highborn Elves", "Wysokie Elfy"),
    ("ID", "Infernal Dwarves", "Krasnoludy Chaosu"),
    ("KoE", "Kingdome of Equitaine", "Bretonia"),
    ("OK", "Ogre Khans", "Ogry"),
    ("OG", "Orcs and Goblins", "Orki i Gobliny"),
    ("SA", "Saurian Ancients", "Lizarmeni"),
    ("SE", "Sylvan Elves", "Leśne Elfy"),
    ("UD", "Undying Dynasties", "Khemri"),
    ("VC", "Vampire Covenant", "Wampiry"),
    ("VS", "Vermin Swarm", "Skaveni"),
    ("WDG", "Warriors of the Dark Gods", "Wojownicy CHaosu")
)


for army in ARMIES_CHOICE:
    Armys.objects.create(
        name = army[1],
        short_name = army[0],
        description = army[2]
    )

from wfb_app.models import Armys


ARMIES_CHOICE = (
    ("BH", "Beast Herds", "Bestie", "https://www.the-ninth-age.com/local/cache-gd2/5a/dac02de101ddc2bd62c58f71a50954.png?1606470875"),
    ("DL", "Demonic Legion", "Demony", "https://www.the-ninth-age.com/local/cache-gd2/f9/a3d0701ccaeebf3cbd6bf1ca809abb.png?1606470875"),
    ("DE", "Dread Elves", "Mroczne Elfy", "https://www.the-ninth-age.com/local/cache-gd2/7b/4caf8f8eca9b789676c3b573cc4786.png?1606470876"),
    ("DH", "Dvarwen Holds", "Krasnoludy", "https://www.the-ninth-age.com/local/cache-gd2/4f/6341694279d2cfd29a159d2a2959b4.png?1606470876"),
    ("EoS", "Empire of Sonnstahl", "Imperium", "https://www.the-ninth-age.com/local/cache-gd2/af/9d71d629ab9545276aa2cca52d7b28.png?1606470876"),
    ("HE", "Highborn Elves", "Wysokie Elfy", "https://www.the-ninth-age.com/local/cache-gd2/3c/cad7ab1c710675a84ae7729ca86dc5.png?1606470876"),
    ("ID", "Infernal Dwarves", "Krasnoludy Chaosu", "https://www.the-ninth-age.com/local/cache-gd2/5d/8c30b756070086c10e7b413fef59b1.png?1606470876"),
    ("KoE", "Kingdome of Equitaine", "Bretonia", "https://www.the-ninth-age.com/local/cache-gd2/d4/4677236a7f62b854b742b285c08ee4.png?1606470876"),
    ("OK", "Ogre Khans", "Ogry", "https://www.the-ninth-age.com/local/cache-gd2/8b/e830f87ffdf53d28d18681b38232d2.png?1606470876"),
    ("OG", "Orcs and Goblins", "Orki i Gobliny", "https://www.the-ninth-age.com/local/cache-gd2/31/22c754b60db51c753d588a4409e9d2.png?1606470876"),
    ("SA", "Saurian Ancients", "Lizarmeni", "https://www.the-ninth-age.com/local/cache-gd2/48/73fcca4e3a6891640e712f68cb24e0.png?1606470877"),
    ("SE", "Sylvan Elves", "Leśne Elfy", "https://www.the-ninth-age.com/local/cache-gd2/8c/fd60bb3ec3c8288ad828e8b7acfab4.png?1606470877"),
    ("UD", "Undying Dynasties", "Khemri", "https://www.the-ninth-age.com/local/cache-gd2/8c/fd60bb3ec3c8288ad828e8b7acfab4.png?1606470877"),
    ("VC", "Vampire Covenant", "Wampiry", "https://www.the-ninth-age.com/local/cache-gd2/1e/7f40ab24cd1cd21ef0541ada409bf2.png?1606470877"),
    ("VS", "Vermin Swarm", "Skaveni", "https://www.the-ninth-age.com/local/cache-gd2/f3/8fb51097ab7fed5d122591e6157d34.png?1606470877"),
    ("WDG", "Warriors of the Dark Gods", "Wojownicy Chaosu", "https://www.the-ninth-age.com/local/cache-gd2/2e/111392397d4922d9b99de0b1f2b9da.png?1606470877")
)


for army in ARMIES_CHOICE:
    Armys.objects.filter(name=army[1]).update(
        name=army[1],
        short_name=army[0],
        description=army[2],
        icon=army[3],
    )

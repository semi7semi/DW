# Generated by Django 3.2 on 2021-05-07 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfb_app', '0002_auto_20210117_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameresults',
            name='opponent_army',
            field=models.CharField(blank=True, choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], default=None, max_length=32, null=True),
        ),
    ]
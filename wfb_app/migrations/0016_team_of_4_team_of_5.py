# Generated by Django 3.2.5 on 2022-01-07 20:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wfb_app', '0015_remove_team_of_3_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team_of_5',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('op1', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op2', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op3', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op4', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op5', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p11', models.IntegerField()),
                ('p12', models.IntegerField()),
                ('p13', models.IntegerField()),
                ('p14', models.IntegerField()),
                ('p15', models.IntegerField()),
                ('p21', models.IntegerField()),
                ('p22', models.IntegerField()),
                ('p23', models.IntegerField()),
                ('p24', models.IntegerField()),
                ('p25', models.IntegerField()),
                ('p31', models.IntegerField()),
                ('p32', models.IntegerField()),
                ('p33', models.IntegerField()),
                ('p34', models.IntegerField()),
                ('p35', models.IntegerField()),
                ('p41', models.IntegerField()),
                ('p42', models.IntegerField()),
                ('p43', models.IntegerField()),
                ('p44', models.IntegerField()),
                ('p45', models.IntegerField()),
                ('p51', models.IntegerField()),
                ('p52', models.IntegerField()),
                ('p53', models.IntegerField()),
                ('p54', models.IntegerField()),
                ('p55', models.IntegerField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tourney5', to='wfb_app.tournaments')),
            ],
        ),
        migrations.CreateModel(
            name='Team_of_4',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('op1', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op2', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op3', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('op4', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p11', models.IntegerField()),
                ('p12', models.IntegerField()),
                ('p13', models.IntegerField()),
                ('p14', models.IntegerField()),
                ('p21', models.IntegerField()),
                ('p22', models.IntegerField()),
                ('p23', models.IntegerField()),
                ('p24', models.IntegerField()),
                ('p31', models.IntegerField()),
                ('p32', models.IntegerField()),
                ('p33', models.IntegerField()),
                ('p34', models.IntegerField()),
                ('p41', models.IntegerField()),
                ('p42', models.IntegerField()),
                ('p43', models.IntegerField()),
                ('p44', models.IntegerField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tourney4', to='wfb_app.tournaments')),
            ],
        ),
    ]

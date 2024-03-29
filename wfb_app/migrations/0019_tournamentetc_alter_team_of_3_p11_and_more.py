# Generated by Django 4.0.3 on 2022-06-06 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfb_app', '0018_alter_team_of_3_p11_alter_team_of_3_p12_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TournamentETC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('player_name_1', models.CharField(max_length=64)),
                ('player_name_2', models.CharField(max_length=64)),
                ('player_name_3', models.CharField(max_length=64)),
                ('player_name_4', models.CharField(max_length=64)),
                ('player_name_5', models.CharField(max_length=64)),
                ('player_name_6', models.CharField(max_length=64)),
                ('player_name_7', models.CharField(max_length=64)),
                ('player_name_8', models.CharField(max_length=64)),
                ('p1', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p2', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p3', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p4', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p5', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p6', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p7', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('p8', models.CharField(choices=[('BH', 'Beast Herds'), ('DL', 'Demonic Legion'), ('DE', 'Dread Elves'), ('DH', 'Dvarwen Holds'), ('EoS', 'Empire of Sonnstahl'), ('HE', 'Highborn Elves'), ('ID', 'Infernal Dwarves'), ('KoE', 'Kingdome of Equitaine'), ('OK', 'Ogre Khans'), ('OG', 'Orcs and Goblins'), ('SA', 'Saurian Ancients'), ('SE', 'Sylvan Elves'), ('UD', 'Undying Dynasties'), ('VC', 'Vampire Covenant'), ('VS', 'Vermin Swarm'), ('WDG', 'Warriors of the Dark Gods')], max_length=16)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p11',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p12',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p13',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p21',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p22',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p23',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p31',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p32',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_3',
            name='p33',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p11',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p12',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p13',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p14',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p21',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p22',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p23',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p24',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p31',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p32',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p33',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p34',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p41',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p42',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p43',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_4',
            name='p44',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p11',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p12',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p13',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p14',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p15',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p21',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p22',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p23',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p24',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p25',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p31',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p32',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p33',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p34',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p35',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p41',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p42',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p43',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p44',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p45',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p51',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p52',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p53',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p54',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
        migrations.AlterField(
            model_name='team_of_5',
            name='p55',
            field=models.IntegerField(choices=[(-3, '-3'), (-2, '-2'), (-1, '-1'), (0, '0'), (1, '1'), (2, '2'), (3, '3')]),
        ),
    ]

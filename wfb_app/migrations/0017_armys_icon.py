# Generated by Django 4.0.1 on 2022-02-04 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wfb_app', '0016_team_of_4_team_of_5'),
    ]

    operations = [
        migrations.AddField(
            model_name='armys',
            name='icon',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
# Generated by Django 5.1.1 on 2024-11-19 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment_portal', '0003_remove_userprofile_has_set_password_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tateam',
            name='ta_team_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]

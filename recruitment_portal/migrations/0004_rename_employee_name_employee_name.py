# Generated by Django 5.1.1 on 2024-10-17 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment_portal', '0003_remove_feedback_interviewer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='employee_name',
            new_name='name',
        ),
    ]
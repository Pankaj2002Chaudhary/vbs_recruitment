# Generated by Django 5.1.1 on 2024-10-08 12:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruitment_portal', '0006_remove_candidate_firstround_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interviewer', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=50)),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='recruitment_portal.candidate')),
            ],
        ),
    ]
